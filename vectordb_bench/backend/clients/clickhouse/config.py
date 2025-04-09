from typing import TypedDict
from pydantic import BaseModel, SecretStr
from ..api import DBConfig, DBCaseConfig, MetricType, IndexType

class ClickhouseConfig(DBConfig):
    user_name: str  = "clickhouse"
    password: SecretStr
    host: str = "localhost"
    port: int = 8123
    db_name: str = "default"

    def to_dict(self) -> dict:
        pwd_str = self.password.get_secret_value()
        return {
            "host": self.host,
            "port": self.port,
            "dbname": self.db_name,
            "user": self.user_name,
            "password": pwd_str
        }


class ClickhouseIndexConfig(BaseModel):

    metric_type: MetricType | None = None

    def parse_metric(self) -> str:
        if not self.metric_type:
            return ""
        return self.metric_type.value

    def parse_metric_str(self) -> str:
        if self.metric_type == MetricType.L2:
            return "L2Distance"
        elif self.metric_type == MetricType.COSINE:
            return "cosineDistance"


class ClickhouseHNSWConfig(ClickhouseIndexConfig, DBCaseConfig):
    M: int | None
    efConstruction: int | None
    ef: int | None = None
    index: IndexType = IndexType.HNSW

    def index_param(self) -> dict:
        return {
            "metric_type": self.parse_metric_str(),
            "index_type": self.index.value,
            "params": {"M": self.M, "efConstruction": self.efConstruction},
        }

    def search_param(self) -> dict:
        return {
            "metric_type": self.parse_metric_str(),
            "params": {"ef": self.ef},
        }