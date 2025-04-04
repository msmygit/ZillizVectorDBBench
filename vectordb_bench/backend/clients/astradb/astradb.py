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

from cassandra import ProtocolVersion, ConsistencyLevel
from cassandra.auth import PlainTextAuthProvider
from cassandra.concurrent import execute_concurrent_with_args
from cassandra.cluster import Cluster, ResultSet, NoHostAvailable, EXEC_PROFILE_DEFAULT, Session, ExecutionProfile
from cassandra.policies import ExponentialReconnectionPolicy

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
        self.astra_token = db_config.get('astra_token')
        self.scb_path = db_config.get('scb_path')
        self.keyspace = db_config['keyspace'].lower()

        self.cluster = Cluster(
            cloud={
                "secure_connect_bundle": self.scb_path,
                "connect_timeout": 30,
            },
            auth_provider=PlainTextAuthProvider(
                "token", self.astra_token
            ),
            protocol_version=ProtocolVersion.V4,
            execution_profiles={EXEC_PROFILE_DEFAULT: ExecutionProfile(request_timeout=60)},
            reconnection_policy=ExponentialReconnectionPolicy(base_delay=1, max_delay=60),
        )
        self.session = self.cluster.connect()
        log.info(f"Connected to {name} cluster")
        self.session.set_keyspace(self.keyspace)

        if drop_old:
            log.info(f"Dropping table: {collection_name} and the index(es)")
            self.session.execute(DROP_INDEX_TEMPLATE%collection_name)
            self.session.execute(DROP_TABLE_TEMPLATE%collection_name)
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
        self.cluster = Cluster(
            cloud={
                "secure_connect_bundle": self.scb_path,
                "connect_timeout": 30,
            },
            auth_provider=PlainTextAuthProvider(
                "token", self.astra_token
            ),
            protocol_version=ProtocolVersion.V4,
            execution_profiles={EXEC_PROFILE_DEFAULT: ExecutionProfile(request_timeout=60)},
            reconnection_policy=ExponentialReconnectionPolicy(base_delay=1, max_delay=60),
        )
        try:
            self.session.set_keyspace(self.keyspace)
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
        """
        Insert the embeddings to the vector database. The default number of embeddings for
        each insert_embeddings is 5000.
        Args:
            embeddings(list[list[float]]): list of embedding to add to the vector database.
            metadatas(list[int]): metadata associated with the embeddings, for filtering.
            **kwargs(Any): vector database specific parameters.
        Returns:
            int: inserted data count
        """
        assert self.session is not None, "session is not initialized"

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
        """
        optimize will be called between insertion and search in performance cases.
        
        Should be blocked until the vectorDB is ready to be tested on
        heavy performance cases.

        Time(insert the dataset) + Time(optimize) will be recorded as "load_duration" metric
        Optimize's execution time is limited, the limited time is based on cases.

        Astra DB vector search indexes are self-optimizing and nearly synchronous and 
        hence we simply sleep for 15 minutes here to play fair game with other DBs that waits to optimize.
        """
        log.info("optimize for search")
        time.sleep(900)

    def search_embedding(
        self,
        query: list[float],
        k: int = 100,
        filters: dict | None = None,
    ) -> list[int]:
        """Get k most similar embeddings to query vector.
        Args:
            query(list[float]): query embedding to look up documents similar to.
            k(int): Number of most similar embeddings to return. Defaults to 100.
            filters(dict, optional): filtering expression to filter the data while searching.
        Returns:
            list[int]: list of k most similar embeddings IDs to the query embedding.
        """
        # filtering search not supported yet
        assert self.session is not None, "session is not initialized"

        statement = self._select.bind([query, k])
        statement.consistency_level = ConsistencyLevel.LOCAL_ONE
        results = self.session.execute(statement)
        return [row.id for row in results]

    def ready_to_load(self):
        pass