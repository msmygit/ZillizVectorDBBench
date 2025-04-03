"""Wrapper around the Astra DB vector database over VectorDB"""
import json
import logging
import os
import time
import urllib.error
import urllib.request
import uuid
from contextlib import contextmanager
from typing import Type
from ..api import DBCaseConfig, VectorDB, DBConfig, EmptyDBCaseConfig, IndexType
from .config import AstraDBConfig
from cassandra import ConsistencyLevel
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, ResultSet, NoHostAvailable, EXEC_PROFILE_DEFAULT, Session
from cassandra.concurrent import ConcurrentExecutorListResults, execute_concurrent_with_args
from cassandra.policies import ExponentialReconnectionPolicy
from cassandra.query import PreparedStatement

BASE_DEV_URL = "https://api.dev.cloud.datastax.com"
BASE_TEST_URL = "https://api.test.cloud.datastax.com"
BASE_PROD_URL = "https://api.astra.datastax.com"
BASE_ASTRA_API_URL = ""

CREATE_TABLE_TEMPLATE = """
CREATE TABLE IF NOT EXISTS %s (
    id INT,
    embedding VECTOR<FLOAT, %s>,
    PRIMARY KEY (id)
);
"""
CREATE_INDEX_TEMPLATE = """
CREATE CUSTOM INDEX IF NOT EXISTS %s_index
ON %s(embedding) USING 'StorageAttachedIndex' WITH OPTIONS = { 'source_model': 'other'};
"""
DROP_TABLE_TEMPLATE = """
DROP TABLE IF EXISTS %s;
"""
DROP_INDEX_TEMPLATE = """
DROP INDEX IF EXISTS %s_index;
"""
INSERT_PREPARED = """
INSERT INTO %s (id, embedding) VALUES (?, ?);
"""
SELECT_PREPARED = """
SELECT id FROM %s ORDER BY embedding ANN OF ? LIMIT ?;
"""

log = logging.getLogger(__name__)

def _get_astra_bundle_url(db_id, token):
    # set up the request
    url = f"{BASE_ASTRA_API_URL}/v2/databases/{db_id}/secureBundleURL"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    req = urllib.request.Request(url, method="POST", headers=headers, data=b"")
    try:
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode())
            # happy path
            if 'downloadURL' in response_data:
                return response_data['downloadURL']
            # handle errors
            if 'errors' in response_data:
                raise Exception(response_data['errors'][0]['message'])
            raise Exception('Unknown error in ' + str(response_data))
    except urllib.error.URLError as e:
        raise Exception(f"Error connecting to Astra API: {str(e)}")

def _get_secure_connect_bundle(token: str, db_id: str, verbose: bool = False) -> str:
    scb_path = f'astra-secure-connect-{db_id}.zip'
    if not os.path.exists(scb_path):
        if verbose: log.info('Downloading Secure Cloud Bundle...')
        url = _get_astra_bundle_url(db_id, token)
        try:
            with urllib.request.urlopen(url) as r:
                with open(scb_path, 'wb') as f:
                    f.write(r.read())
        except urllib.error.URLError as e:
            raise Exception(f"Error downloading secure connect bundle for DB ID: {db_id}: {str(e)}")
    return scb_path

def _connect_astra(self, token: str, db_id: str, scb_path: str = None, verbose: bool = False) -> Session:
    cloud_config = {
        'secure_connect_bundle': scb_path if scb_path else _get_secure_connect_bundle(token, db_id, verbose)
    }
    auth_provider = PlainTextAuthProvider('token', token)
    reconnection_policy = ExponentialReconnectionPolicy(base_delay=1, max_delay=60)
    self.cluster = Cluster(
        cloud=cloud_config,
        auth_provider=auth_provider,
        reconnection_policy=reconnection_policy
    )
    self.session = self.cluster.connect()
    if verbose: log.info(f"Connected to Astra DB {db_id}")
    return self.session

def _maybe_create_keyspace(self, db_id, token, verbose: bool = False):
    url = f"{BASE_ASTRA_API_URL}/v2/databases/{db_id}/keyspaces/{self.keyspace}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "name": self.keyspace
    }).encode('utf-8')

    req = urllib.request.Request(url, method="POST", headers=headers, data=data)

    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 201:
                if verbose: log.info(f"Keyspace '{self.keyspace}' created or verified")
                # Wait for the keyspace to be available (max 10 seconds)
                start_time = time.time()
                while time.time() - start_time < 10:
                    try:
                        self.session.execute(f"USE {self.keyspace}")
                        break
                    except BaseException:
                        time.sleep(0.1)
                else:
                    raise Exception(f"Keyspace '{self.keyspace}' creation successful, but still unavailable after 10 seconds")
            else:
                raise Exception(f"Failed to create keyspace: {response.read().decode()}")
    except urllib.error.HTTPError as e:
        raise Exception(f"Failed to create keyspace: {e.read().decode()}")

class AstraDB(VectorDB):
    def __init__(
        self,
        dim: int,
        db_config: dict,
        db_case_config: DBCaseConfig | None,
        collection_name: str = "vectordb_bench_collection",
        drop_old: bool = False,
        name: str = "Astra DB",
        **kwargs,
    ) -> None:
        self.astra_db_id = db_config.get('astra_db_id', None)
        self.astra_db_endpoint = db_config.get('astra_endpoint', None)
        self.astra_token = db_config.get('astra_token')
        self.keyspace = db_config['keyspace']
        self.table = collection_name
        self.scb_path = db_config['scb_path']
        self.case_config = db_case_config
        self.verbose = db_config.get('verbose')
        self.astra_env = (db_config['astra_env']).lower()
        BASE_ASTRA_API_URL = BASE_DEV_URL if self.astra_env == 'dev' else BASE_TEST_URL if self.astra_env == 'test' else BASE_PROD_URL

        if self.astra_db_id and self.astra_endpoint:
            raise ValueError("Both astra_db_id and astra_endpoint cannot be provided simultaneously.")

        if self.astra_endpoint:
            import re
            match = re.search(r'https://([0-9a-f-]{36})-', self.astra_endpoint)
            if not match:
                raise ValueError("Invalid astra_endpoint format. Expected UUID not found.")
            self.astra_db_id = match.group(1)

        if self.astra_db_id:
            try:
                uuid.UUID(self.astra_db_id)
            except ValueError:
                raise ValueError(f"Invalid astra_db_id: {self.astra_db_id}. It must be a valid UUID.")

        if not self.astra_db_id:
            raise Exception('astra_db_id not set')

        if self.verbose: print(f'Connecting to Astra DB {self.astra_db_id}')
        self.session = _connect_astra(self.astra_token, self.astra_db_id, self.scb_path, self.verbose)
        self.session.default_timeout = 60  # this is the client timeout, server still has internal timeouts

        _maybe_create_keyspace(self.astra_db_id, self.astra_token, self.verbose)
        self.session.set_keyspace(self.keyspace)

        if drop_old:
            log.info(f"Dropping table: {collection_name}")
            self.session.execute(DROP_TABLE_TEMPLATE%collection_name)
            self.session.execute(DROP_INDEX_TEMPLATE%collection_name)
        self.session.execute(CREATE_TABLE_TEMPLATE%(collection_name, dim))
        self.session.execute(CREATE_INDEX_TEMPLATE%(collection_name, collection_name))
        self.session.shutdown()

    @classmethod
    def config_cls(cls) -> Type[DBConfig]:
        return AstraDBConfig

    @classmethod
    def case_config_cls(cls, index_type: IndexType | None = None) -> Type[DBCaseConfig]:
        return EmptyDBCaseConfig

    @contextmanager
    def init(self):
        reconnection_policy = ExponentialReconnectionPolicy(base_delay=1, max_delay=60)
        cluster = Cluster(
            cloud=self.scb_path,
            auth_provider=self.auth_provider,
            reconnection_policy=reconnection_policy
        )
        self.session = cluster.connect()
        try:
            self.session.set_keyspace(self.keyspace)
            self.session.default_timeout = 60  # this is the client timeout, server still has internal timeouts
            self._insert = self.session.prepare(INSERT_PREPARED%self.table)
            self._select = self.session.prepare(SELECT_PREPARED%self.table)
            log.info("prepare completed")
            yield
        finally:
            log.info("shutting down")
            self.session.shutdown()

    def insert_embeddings(
        self,
        embeddings: list[list[float]],
        metadata: list[int],
        **kwargs,
    ) -> (int, Exception):

        params = [(metadata[i], embeddings[i]) for i in range(len(metadata))]
        results = execute_concurrent_with_args(self.session, self._insert, params, concurrency=16, raise_on_first_error=False)
        successful_results = list(filter(lambda result: result.success, results))
        if len(successful_results) == len(results):
            return len(successful_results), None
        else:
            failed_results = filter(lambda result: not result.success, results)
            error = next(failed_results).result_or_exc
            log.warning(f"Failed to insert data, error: {error}")   
            return len(successful_results), error

    def optimize(self):
        """Astra DB vector search indexes are self-optimizing and nearly synchronous"""
        log.info("optimize for search")
        # wait for 15 minutes for the index to be ready as there is no
        # external facing method to check the index status
        time.sleep(900)

    def search_embedding(
        self,
        query: list[float],
        k: int = 100,
        filters: dict | None = None,
    ) -> list[int]:
        # filtering search not supported yet

        statement = self._select.bind([query, k])
        statement.consistency_level = ConsistencyLevel.LOCAL_ONE
        results = self.session.execute(statement)
        return [row.id for row in results]

    def ready_to_load(self):
        pass