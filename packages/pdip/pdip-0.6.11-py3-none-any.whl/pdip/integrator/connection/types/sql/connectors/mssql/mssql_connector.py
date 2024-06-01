import os

import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from ...base import SqlConnector
from .....domain.types.sql.configuration.base import SqlConnectionConfiguration


class MssqlConnector(SqlConnector):
    def __init__(self, config: SqlConnectionConfiguration):
        self.config: SqlConnectionConfiguration = config
        if self.config.ConnectionString is not None and self.config.ConnectionString != '' and not self.config.ConnectionString.isspace():
            self.connection_string = self.config.ConnectionString
        else:
            if self.config.Driver is None or self.config.Driver == '':
                self.config.Driver = self.find_driver_name()
            app_name = os.getenv('MSSQL_APP_NAME', 'pdi')
            self.connection_string = 'DRIVER={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s;APP=%s' % (
                self.config.Driver, self.config.Server.Host, self.config.Database,
                self.config.BasicAuthentication.User, self.config.BasicAuthentication.Password, app_name)
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = pyodbc.connect(self.connection_string)  # ,ansi=True)
        # self.connection.setencoding(encoding='utf-8')
        self.cursor = self.connection.cursor()
        self.cursor.setinputsizes([(pyodbc.SQL_WVARCHAR, 0, 0)])

    def disconnect(self):
        try:
            if self.cursor is not None:
                self.cursor.close()

            if self.connection is not None:
                self.connection.close()
        except Exception:
            pass

    def get_connection(self):
        return self.connection

    def get_engine_connection_url(self):
        connection_url = URL.create(
            "mssql+pyodbc",
            query={"odbc_connect": self.connection_string}
        )
        return connection_url

    def get_engine(self):
        connection_url = self.get_engine_connection_url()
        engine = create_engine(connection_url)
        return engine

    def find_driver_name(self):
        drivers = pyodbc.drivers()
        driver_name = None
        driver_names = [x for x in drivers if 'for SQL Server' in x]
        if driver_names:
            driver_name = list(reversed(driver_names))[0]
        else:

            driver_names = [
                x for x in drivers if 'SQL Server' in x or 'FreeTDS' in x]
            if driver_names:
                driver_name = list(reversed(driver_names))[0]
            else:
                driver_name = drivers[0]
        return driver_name

    def execute_many(self, query, data):
        self.cursor.fast_executemany = True
        try:
            self.cursor.executemany(query, data)
            self.connection.commit()
            return self.cursor.rowcount
        except Exception as error:
            try:
                self.connection.rollback()
                self.cursor.fast_executemany = False
                self.cursor.executemany(query, data)
                self.connection.commit()
                return self.cursor.rowcount
            except Exception as error:
                self.connection.rollback()
                self.cursor.close()
                raise
