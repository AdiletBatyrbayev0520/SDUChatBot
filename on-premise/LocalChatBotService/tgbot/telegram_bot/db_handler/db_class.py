import asyncpg
import logging
from typing import Any, List

class PostgresHandler:
    def __init__(self, database_url: str):
        """
        Initialize the PostgresHandler.

        :param database_url: The database connection URL.
        """
        self.database_url = database_url
        self.pool = None
        self.logger = logging.getLogger(__name__)

    async def connect(self):
        """
        Create a connection pool to the PostgreSQL database.
        """
        try:
            self.pool = await asyncpg.create_pool(dsn=self.database_url, min_size=1, max_size=10)
            self.logger.info("Successfully connected to the PostgreSQL database.")
        except Exception as e:
            self.logger.error("Error connecting to the PostgreSQL database: %s", str(e))
            raise

    async def disconnect(self):
        """
        Close the connection pool.
        """
        if self.pool:
            await self.pool.close()
            self.logger.info("Connection to the PostgreSQL database has been closed.")

    async def execute(self, query: str, *args: Any) -> None:
        """
        Execute a query that does not return a result (e.g., INSERT, UPDATE, DELETE).

        :param query: SQL query to execute.
        :param args: Query parameters.
        """
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, *args)

    async def fetch(self, query: str, *args: Any) -> List[asyncpg.Record]:
        """
        Execute a query and fetch all results (e.g., SELECT).

        :param query: SQL query to execute.
        :param args: Query parameters.
        :return: List of records.
        """
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetchrow(self, query: str, *args: Any) -> asyncpg.Record:
        """
        Execute a query and fetch a single row.

        :param query: SQL query to execute.
        :param args: Query parameters.
        :return: A single record.
        """
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def fetchval(self, query: str, *args: Any) -> Any:
        """
        Execute a query and fetch a single value.

        :param query: SQL query to execute.
        :param args: Query parameters.
        :return: A single value.
        """
        async with self.pool.acquire() as connection:
            return await connection.fetchval(query, *args)
