from adbc_driver_manager.dbapi import Connection
from aita.datasource.sql import SqlDataSource
from pydantic import Field
from typing import Optional
import adbc_driver_postgresql.dbapi


class PostgreSqlDataSource(SqlDataSource):
    connection_url: str = Field(..., description="Connection URL")

    def __init__(
        self,
        connection_url: Optional[str] = None,
        **kwargs,
    ):
        if not connection_url:
            user = kwargs.get("user")
            password = kwargs.get("password")
            host = kwargs.get("host")
            port = kwargs.get("port")
            database = kwargs.get("database")
            connection_url = self.build_connection_url(
                user=user,
                password=password,
                host=host,
                port=port,
                database=database,
                **kwargs,
            )
        super().__init__(connection_url=connection_url)

    def build_connection_url(
        self,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        **kwargs,
    ) -> str:
        connection_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        if kwargs:
            connection_url += "?" + "&".join([f"{k}={v}" for k, v in kwargs.items()])
        return connection_url

    def connect(self) -> Connection:
        return adbc_driver_postgresql.dbapi.connect(self.connection_url)
