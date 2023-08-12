"""Classes to manipulate dataframes.
"""

from typing import Optional, Literal, Union, List, Any, Dict
import pandas as pd
import pandera as pa
from data_engineering.data_types.files import File
from data_engineering.connections.database import SQLDatabase


class PDDataframe:
    """Creates a Pandas Dataframe object with a Panderas schema.

    If a Panderas DataFrameSchema is provided each time the dataframe is
    assigned, it will validate the schema of the dataframe. It can be used to
    upload and download a dataframe as an csv file or sql table.

    Attributes:
        dataframe (pd.DataFrame): Pandas Dataframe
        schema (pa.DataFrameSchema): Panderas Dataframe Schema that validates the
            structure of the dataframe.
    """

    def __init__(
        self, dataframe: pd.DataFrame, schema: Optional[pa.DataFrameSchema] = None
    ) -> None:
        """Defines a dataframe with an schema.

        Args:
            dataframe (pd.DataFrame): Pandas Dataframe
            schema (pa.DataFrameSchema, optional): Panderas Dataframe Schema
                that validates the structure of the dataframe.. Defaults to
                None.
        """
        self.dataframe = dataframe
        self.schema = schema
        self._dataframe: pd.DataFrame

    @property
    def dataframe(self) -> pd.DataFrame:
        """Used to get the value of the dataframe attribute.

        Returns:
            pd.DataFrame: Pandas Dataframe
        """
        return self._dataframe

    @dataframe.setter
    def dataframe(self, dataframe: pd.DataFrame) -> None:
        """Used to assign the value of the dataframe attribute. If there is an
        schema it will validate the structure of the dataframe.

        Args:
            dataframe (pd.DataFrame): Pandas Dataframe
        """
        if self.schema is not None:
            self.schema.validate(dataframe)
        self._dataframe = dataframe

    def to_csv(self, file: File, index: bool = False) -> None:
        """Save a Pandas Dataframe as a csv file.

        Args:
            file (File): File object that has the target file data
            index (bool, optional): Load the index as a column. Defaults to
                False.
        """
        self.dataframe.to_csv(file.path, index=index)

    def read_csv(
        self, file: File, index_col: Optional[int] = None, parse_dates: bool = False
    ):
        """Downloads a csv file and transforms it into a Pandas Dataframe.

        Args:
            file (File): File object that has the origin file data
            index_col (Optional[int], optional): column in the csv file to be
                used as a index. If None index will be generated. Defaults to
                None.
            parse_dates (bool, optional): parse date like columns. Defaults to
                False.
        """
        self.dataframe = pd.read_csv(
            file.path, index_col=index_col, parse_dates=parse_dates
        )

    def to_sql(
        self,
        table_name: str,
        sql_database: SQLDatabase,
        if_exists: Literal["fail", "replace", "append"],
        index: bool = False,
    ) -> None:
        """Uploads a Pandas Dataframe to a SQL Database.

        Args:
            table_name (str): name of the table in the database
            sql_database (SQLDatabase): SQLDatabase object connected to the
                target database.
            if_exists (Literal["fail", "replace", "append"]): how to behave if
                the table already exists
            index (bool, optional): if the index has to be load to the
                database. Defaults to False.
        """
        sql_connector = sql_database.connector
        self.dataframe.to_sql(
            table_name, sql_connector, if_exists=if_exists, index=index
        )

    def read_sql(
        self,
        sql: str,
        sql_database: SQLDatabase,
        index_col: Union[str, List[str], None] = None,
        parse_dates: Union[
            List[str], Dict[str, str], Dict[str, Dict[str, Any]], None
        ] = None,
    ):
        """Downloads a Pandas Dataframe from the SQL Database.

        Args:
            sql (str): query or table name
            sql_database (SQLDatabase): SQLDatabase object connected to the
                origin database.
            index_col (Union[str, List[str], None], optional): column to set as
                an index. If None there index will be generated. Defaults to
                None.
            parse_dates (Union[ List[str], Dict[str, str], Dict[str, Dict[str,
                Any]], None ], optional): columns to parse as dates. Defaults
                to None.
        """
        sql_connector = sql_database.connector
        self.dataframe = pd.read_sql(
            sql, sql_connector, index_col=index_col, parse_dates=parse_dates
        )
