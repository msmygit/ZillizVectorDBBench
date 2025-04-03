from pydantic import SecretStr
from ..api import DBConfig

class AstraDBConfig(DBConfig):
    """
    AstraDB configuration class.

    Attributes:
        keyspace (Optional[str]): The keyspace to use in the database. This program will create it if it doesn't exist. Defaults to 'default_keyspace'.
        astra_endpoint (Optional[str]): The Astra DB cluster's endpoint URL (required for Astra DB connections).
        astra_db_id (Optional[str]): The Astra database ID (required for Astra DB connections).
        astra_token (Optional[str]): The Astra authentication token (required for Astra DB connections).
        scb_path (Optional[str]): The path to the secure connect bundle (required for Astra DB connections).
        verbose (Optional[bool]): Whether to print verbose output. Defaults to False.
        astra_env (Optional[str]): The Astra environment. Defaults to 'prod'.
    """
    astra_db_id: str | None = None,
    astra_endpoint: str | None = None,
    astra_token: SecretStr | None = None, # This starts with AstraCS:...
    scb_path: str | None = None # This is the path to the secure connect bundle
    keyspace: str | None = "default_keyspace"
    verbose: bool | None = False
    astra_env: str | None = "prod"

    def to_dict(self) -> dict:
        return {
            "astra_db_id": self.astra_db_id,
            "astra_endpoint": self.astra_endpoint,
            "astra_token": self.astra_token.get_secret_value(),
            "scb_path": self.scb_path,
            "keyspace": self.keyspace,
            "verbose": self.verbose,
            "astra_env": self.astra_env
        }