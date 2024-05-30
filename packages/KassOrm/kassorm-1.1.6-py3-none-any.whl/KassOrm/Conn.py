import mysql.connector
import logging
from mysql.connector import errorcode
import mysql.connector.pooling


class Conn:

    def __init__(self, conn=None) -> None:
        logging.basicConfig(
            filename="logs/KassOrm.log",
            level=logging.CRITICAL,
            format="%(asctime)s - %(levelname)s - Conn() -%(message)s",
        )
        self.query = None
        self.params = None
        self.cursor = None

        config_pool = conn
        config_pool["pool_size"] = conn.get("pool_size", 5)
        config_pool["pool_name"] = conn.get("pool_name", "ormkass_pool")
        config_pool["connect_timeout"] = conn.get("connect_timeout", 30)
        config_pool["pool_reset_session"] = conn.get("pool_reset_session", True)

        try:
            self.conn_pool = mysql.connector.pooling.MySQLConnectionPool(**config_pool)
        except mysql.connector.Error as err:
            self.__handle_error(err)

    def set_query(self, query: str, params: dict = None) -> "Conn":
        """Define a consulta SQL e seus parâmetros.

        Args:
            query (str): Consulta SQL.
            params (dict, optional): Parâmetros da consulta. Defaults to None.

        Returns:
            Conn: Instância da classe Conn.

        """
        self.query = query
        self.params = params
        return self

    def execute(self) -> "Conn":
        """Executa a consulta definida usando a conexão do pool.

        Returns:
            Conn: Instância da classe Conn.
        """
        self.conn = self.conn_pool.get_connection()
        if self.conn and self.conn.is_connected():
            self.cursor = self.conn.cursor(dictionary=True, buffered=True)
            return self
        self.__handle_error(Exception("Error connecting to the database"))

    def fetch_all(self) -> list[dict] | None:
        """Executa a consulta e recupera todas as linhas do resultado.

        Returns:
            list[dict] or None: Lista de dicionários representando as linhas do resultado.

        """
        self.cursor.execute(self.query, params=self.params)
        data = self.cursor.fetchall() if self.cursor.with_rows else None
        self.__close_connection()
        return data

    def fetch_one(self) -> dict | None:
        """Executa a consulta e recupera a primeira linha do resultado.

        Returns:
            dict or None: Dicionário representando a primeira linha do resultado.
        """
        self.cursor.execute(self.query, params=self.params)
        data = self.cursor.fetchone() if self.cursor.with_rows else None
        self.__close_connection()
        return data

    def insert(self, many=False) -> list[int] | int:
        """Executa uma operação de inserção no banco de dados.

        Args:
            many (bool, optional): Indica se é uma inserção de vários registros. Defaults to False.

        Returns:
            list[int] or int: Lista de IDs gerados ou ID gerado pela inserção.
        """
        if many:
            self.cursor.executemany(self.query, self.params)
            lastid = self.cursor.lastrowid
            last_ids = [lastid + x for x in range(len(self.params))]
        else:
            self.cursor.execute(self.query, params=self.params)
            last_ids = self.cursor.lastrowid
        self.__commit_and_close_connection()
        return last_ids

    def exec(self):
        return self.__exec_query()

    def create(self) -> bool:
        """Executa uma operação de criação (CREATE) no banco de dados.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        return self.__exec_query()

    def drop(self) -> bool:
        return self.__exec_query()

    def update(self) -> bool:
        """Executa uma operação de atualização (UPDATE) no banco de dados.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        return self.__exec_query()

    def delete(self) -> bool:
        """Executa uma operação de exclusão (DELETE) no banco de dados.

        Returns:
             bool: True se a operação for bem-sucedida, False caso contrário.
        """
        return self.__exec_query()

    def __exec_query(self) -> bool:
        """Método interno para executar consultas (CREATE, UPDATE, DELETE).

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        try:
            self.cursor.execute(self.query, self.params)
            self.__commit_and_close_connection()
            return True
        except mysql.connector.Error as err:
            return self.__handle_error(err)

    def __commit_and_close_connection(self) -> None:
        """Método interno para realizar o commit e fechar a conexão."""
        self.conn.commit()
        self.__close_connection()

    def __close_connection(self) -> None:
        """Método interno para fechar a conexão e o cursor."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def __handle_error(self, err) -> None:
        """Método interno para lidar com erros de conexão.

        Args:
            err (_type_): erro gerado
        """
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logging.error("Something is wrong with your user name or password")
            # raise Exception("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logging.error("Database does not exist")
            # raise Exception("Database does not exist")
        else:
            logging.error(err)
            # raise Exception(err)

        return err
