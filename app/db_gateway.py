import logging
import time
from abc import ABC, abstractmethod

import psycopg
import schemas
import settings

SEND_TIMEOUT = 10
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


class DBStrategy(ABC):
    @abstractmethod
    def read_fibonacci(self):
        pass

    @abstractmethod
    def insert_fibonacci(self, sequences):
        pass


class PostgresStrategy(DBStrategy):
    def __init__(self):
        self.user = settings.Settings.POSTGRES_USER
        self.password = settings.Settings.POSTGRES_PASSWORD
        self.db = settings.Settings.POSTGRES_DB
        self.host = settings.Settings.POSTGRES_HOST
        self.port = settings.Settings.POSTGRES_PORT
        self._prep_db()

    def read_fibonacci(self):
        read_statement = "select * from fibonacci"
        with psycopg.connect(
            (
                f"host={self.host} port={self.port} "
                f"dbname={self.db} user={self.user} "
                f"password={self.password}"
            ),
            autocommit=True,
        ) as conn:
            result = conn.execute(read_statement).fetchall()
            rows = []
            for row in result:
                rows.append(
                    schemas.Output(
                        id=row[0], datetime=row[1], fibonacci=row[2]
                    ).model_dump()
                )
            return rows

    def insert_fibonacci(self, datetime, fibonacci):
        insert_statement = f"""
            INSERT INTO fibonacci (datetime, fibonacci)
            VALUES ('{datetime}', '{fibonacci}');
        """

        self._execute_db_statement(insert_statement)

    def _prep_db(self):
        create_table_statement = """
            CREATE TABLE IF NOT EXISTS fibonacci (
                id SERIAL PRIMARY KEY,
                datetime VARCHAR(255),
                fibonacci TEXT
            );
        """

        self._execute_db_statement(create_table_statement)

    def _execute_db_statement(self, statement):
        """
        Execute a database statement with retry logic.

        This method attempts to execute a given SQL statement on a PostgreSQL
        database. It includes retry logic to handle transient errors that may
        occur during the execution. The method will retry the execution up to
        a maximum number of retries defined by MAX_RETRIES. If the statement
        cannot be executed successfully after the maximum number of retries,
        a Exception is raised.

        Args:
            statement (str): The SQL statement to be executed.

        Raises:
            Exception: If the statement cannot be executed after
            the maximum number of retries.

        Logs:
            Logs an error message if an error occurs during the execution of
            the statement.
            Logs an info message indicating the retry delay before each retry
            attempt.
            Logs an error message if the statement fails to execute after the
            maximum number of retries.
        """
        retries = 0
        while retries < MAX_RETRIES:
            try:
                with psycopg.connect(
                    (
                        f"host={self.host} port={self.port} "
                        f"dbname={self.db} user={self.user} "
                        f"password={self.password}"
                    ),
                    autocommit=True,
                ) as conn:
                    conn.execute(statement)
                return
            except psycopg.Error as e:
                retries += 1
                logging.error(f"Error executing database statement: {e}")
                logging.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
        else:
            logging.error(
                (
                    "Failed to execute database statement after multiple "
                    "retries. Please check the database connection and "
                    "configuration."
                )
            )
            raise Exception("Failed to execute database statement")


class JSONStrategy(DBStrategy):
    def __init__(self):
        self._data = []

    def read_fibonacci(self):
        return self._data

    def insert_fibonacci(self, datetime, fibonacci):
        self._data.append({"datetime": datetime, "fibonacci": fibonacci})


class DBGateway:
    def __init__(self):
        if settings.Settings.DB_SOURCE == "postgres":
            self.strategy = PostgresStrategy()
        elif settings.Settings.DB_SOURCE == "json":
            self.strategy = JSONStrategy()
        else:
            raise Exception(
                f"Invalid DB source: {settings.Settings.DB_SOURCE}. "
                "Please set the DB_SOURCE environment variable to 'postgres' "
                "or 'json'."
            )

    def read_fibonacci(self):
        return self.strategy.read_fibonacci()

    def insert_fibonacci(self, datetime, fibonacci):
        self.strategy.insert_fibonacci(datetime, fibonacci)
