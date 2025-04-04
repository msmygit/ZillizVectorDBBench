from pydantic import SecretStr
from ..api import DBConfig
import os

class AstraDBConfig(DBConfig):
    """
    AstraDB configuration class.

    Attributes:
        astra_token (str): The Astra authentication token. This can also be set using the ASTRA_API_KEY environment variable.
        scb_path (str): The path to the secure connect bundle. This can also be set using the ASTRA_SCB_PATH environment variable.
        keyspace (Optional[str]): The keyspace to use in the database. This program will create it if it doesn't exist. Defaults to 'default_keyspace'.
    """
    # This starts with AstraCS:...
    astra_token: SecretStr | None = os.environ.get("ASTRA_API_KEY", None)
    # This is the path to the secure connect bundle
    scb_path: str | None = os.environ.get("ASTRA_SCB_PATH", None)
    keyspace: str | None = "default_keyspace"

    def to_dict(self) -> dict:
        return {
            "astra_token": self.astra_token.get_secret_value(),
            "scb_path": self.scb_path,
            "keyspace": self.keyspace
        }