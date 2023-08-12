"""Classes to connect to a database.

This module provides the necesary classes to connect to a database, all of them
derived from the base class SQLDatabase.
"""
from abc import abstractmethod, ABC
from typing import Optional
from sqlalchemy import Engine, create_engine




class SQLDatabase(ABC): # pylint: disable=too-few-public-methods
    """Uploads and downloads dataframes to a SQL database.

    Abstract class to be used by any data source class that can download and
    upload dataframe to a SQL database.

    Attributes:
        database_name (str): database name

    It implements two methods from DataframeDataSource: upload_df and
    download_df.
    """

    def __init__(self, database_name: str) -> None:
        """Defines a sql database connection.

        Args:
            database_name (str): database name
        """
        self.database_name = database_name
        self.connector = self._get_connector()

    @property
    @abstractmethod
    def _database_uri(self) -> str:
        """str: SQLAlchemy database url"""

    def _get_connector(self) -> Engine:
        """Returns the connector used to interact to the SQL database.

        Returns:
            Engine: SQLAlchemy Engine
        """
        return create_engine(self._database_uri)


class AdvancedSQLClient(SQLDatabase): # pylint: disable=too-few-public-methods
    """Uploads and downloads dataframes to a Complex SQL database.

    Can be used for SQLServer, Postgresql, etc.

    Attributes:
        database_name (str): database name
        dialect (str): database dialect
        host (str): database dialect
        user (str): database user
        password (str): database password
        driver (Optional[str], optional): database driver. Defaults to None.
    """

    def __init__( # pylint: disable=too-many-arguments
        self,
        database_name: str,
        dialect: str,
        host: str,
        user: str,
        password: str,
        driver: Optional[str] = None,
    ) -> None:
        """Initilizes a sql database connection.

        Args:
            database_name (str): database name
            dialect (str): database dialect
            host (str): database host
            user (str): database user
            password (str): database password
            driver (Optional[str], optional): database driver. Defaults to None.
        """
        self.dialect = dialect
        self.host = host
        self.user = user
        self.password = password
        self.driver = driver
        super().__init__(database_name)

    @property
    def _database_uri(self) -> str:
        return f"{self.dialect}://{self.user}:{self.password}@{self.host}/{self.database_name}{''if not self.driver else f'?driver={self.driver}'}"  # pylint: disable=line-too-long


class SQLiteClient(SQLDatabase): # pylint: disable=too-few-public-methods
    """Uploads and downloads dataframes to a SQLite database.

    Attributes:
        database_name (str): database name
    """

    @property
    def _database_uri(self) -> str:
        return f"sqlite:///{self.database_name}"
