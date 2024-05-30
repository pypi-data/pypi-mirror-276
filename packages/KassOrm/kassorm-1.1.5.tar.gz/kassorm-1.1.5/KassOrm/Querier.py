import json
import os
from .Conn import Conn
from datetime import datetime


class Export:

    def __init__(self) -> None:
        pass

    def toCsv(self):
        return

    def toTxt(self):
        return

    def toXlsx(self):
        return

    def toDataframe(self):
        return

    def toJson(self):
        return


class Utils:

    def __init__(self) -> None:
        pass

    def beginTransaction(self):
        return

    def endTransaction(self):
        return


class Relationship:

    def __init__(self) -> None:
        pass

    def innerJoin(self):
        return self

    def leftJoin(self):
        return self

    def join(self):
        return self


class Querier:

    def __init__(self, conn: dict) -> None:

        self.conn = Conn(conn=conn)

        self.table_name = None
        self.columns = []
        self.wheres_cols = []
        self.wheres_param = []
        self.limit_number = None
        self.offset_number = None
        self.groupby = None
        self.orderby = None

    def selectRaw(self, query: str) -> list[dict]:
        """
        Executa uma consulta SQL bruta e retorna o resultado.

        Args:
            query (str): A consulta SQL bruta.

        Returns:
            list[dict]: Uma lista de dicionários representando os resultados da consulta.
        """
        return self.conn.set_query(query=query).execute().fetch_all()

    def table(self, table: str) -> "Querier":
        """
        Define a tabela para a consulta.

        Args:
            table (str): O nome da tabela.

        Returns:
            Querier: A instância atual da classe.
        """
        self.table_name = table
        return self

    def select(self, cols: str | list[str] = "*") -> "Querier":
        """
        Especifica colunas a serem selecionadas na consulta.

        Args:
            cols (str | list[str]): Colunas a serem selecionadas. Pode ser uma string única ou uma lista de strings.

        Returns:
            Querier: A instância atual da classe.
        """
        if type(cols) == list:
            for col in cols:
                self.columns.append(col)
        else:
            self.columns.append(cols)

        return self

    def notSelect(self, cols: str | list[str]) -> "Querier":
        """
        Exclui colunas especificadas da consulta.

        Args:
            cols (str | list[str]): Colunas a serem excluídas da seleção.

        Returns:
            Querier: A instância atual da classe.
        """
        return self

    def __where(self, conditional: list[dict] | dict, operator: str):

        if type(conditional) == dict:
            conditional = [conditional]

        for item in conditional:

            if isinstance(item, dict):
                idx = len(self.wheres_cols)
                col = list(item.keys())[0]
                key_param = f"{col}_{idx}"

                operatorloop = operator if idx > 0 else ""

                query = f" {operatorloop} {col} = %({key_param})s"

                self.wheres_cols.append(query)
                self.wheres_param.append({key_param: item[col]})

            elif isinstance(item, str):
                operator = item
                continue

    def where(self, conditional: list[dict] | dict) -> "Querier":
        """
        Adiciona cláusulas WHERE à consulta.

        Args:
            conditional (list[dict] | dict): Condição da cláusula WHERE. Pode ser um dicionário ou uma lista de dicionários.

        Returns:
            Querier: A instância atual da classe.
        """
        self.__where(conditional, "AND")
        return self

    def orWhere(self, conditional: list[dict] | dict) -> "Querier":
        """
        Adiciona cláusulas OR WHERE à consulta.

        Args:
            conditional (list[dict] | dict): Condição da cláusula WHERE. Pode ser um dicionário ou uma lista de dicionários.

        Returns:
            Querier: A instância atual da classe.
        """
        self.__where(conditional, "OR")
        return self

    def __whereIn(self, column: str, values: list[str], operator: str, notin=False):
        id = len(self.wheres_cols)
        notin = " NOT IN" if notin else "IN"

        operator = operator if id > 0 else ""

        bind_values = []
        for value in values:
            id_param = len(self.wheres_param)
            key_param = f"{column}_{id}{id_param}"
            bind_values.append(f"%({key_param})s")

            self.wheres_param.append({key_param: value})

        join_values = ", ".join(bind_values)
        query = f"{operator} {column} {notin} ({join_values})"
        self.wheres_cols.append(query)

    def whereIn(self, column: str, values: list[str]) -> "Querier":
        """
        Adiciona cláusulas WHERE IN à consulta.

        Args:
            column (str): Nome da coluna.
            values (list[str]): Lista de valores para a cláusula IN.

        Returns:
            Querier: A instância atual da classe.
        """
        self.__whereIn(column, values, "AND", False)
        return self

    def orWhereIn(self, column: str, values: list[str]) -> "Querier":
        """
        Adiciona cláusulas OR WHERE IN à consulta.

        Args:
            column (str): Nome da coluna.
            values (list[str]): Lista de valores para a cláusula IN.

        Returns:
            Querier: A instância atual da classe.
        """
        self.__whereIn(column, values, "OR", False)
        return self

    def whereNotIn(self, column: str, values: list[str]) -> "Querier":
        """
        Adiciona cláusulas WHERE NOT IN à consulta.

        Args:
            column (str): Nome da coluna.
            values (list[str]): Lista de valores para a cláusula NOT IN.

        Returns:
            Querier: A instância atual da classe.
        """
        self.__whereIn(column, values, "AND", True)
        return self

    def orWhereNotIn(self, column: str, values: list[str]) -> "Querier":
        """
        Adiciona cláusulas OR WHERE NOT IN à consulta.

        Args:
            column (str): Nome da coluna.
            values (list[str]): Lista de valores para a cláusula NOT IN.

        Returns:
            Querier: A instância atual da classe.
        """
        self.__whereIn(column, values, "OR", True)
        return self

    def __whereIsNull(self, column: str, operator: str, notnull: bool = False):
        idx = len(self.wheres_cols)
        notnull = "IS NULL" if notnull == False else "IS NOT NULL"
        op = operator if idx > 0 else ""
        query = f" {op} {column} {notnull}"
        self.wheres_cols.append(query)

    def whereIsNull(self, column: str) -> "Querier":
        """
        Adiciona cláusulas WHERE IS NULL à consulta.

        Args:
            column (str): Nome da coluna.

        Returns:
            Querier: A instância atual da classe.
        """
        self.__whereIsNull(column, "AND", False)
        return self

    def orWhereIsNull(self, column: str) -> "Querier":
        """
        Adiciona cláusulas OR WHERE IS NULL à consulta.

        Args:
            column (str): Nome da coluna.

        Returns:
            Querier: A instância atual da classe.
        """
        self.__whereIsNull(column, "OR", False)
        return self

    def whereIsNotNull(self, column: str) -> "Querier":
        """
        Adiciona cláusulas WHERE IS NOT NULL à consulta.

        Args:
            column (str): Nome da coluna.

        Returns:
            Querier: A instância atual da classe.
        """
        self.__whereIsNull(column, "AND", True)
        return self

    def orWhereIsNotNull(self, column: str) -> "Querier":
        """
        Adiciona cláusulas OR WHERE IS NOT NULL à consulta.

        Args:
            column (str): Nome da coluna.

        Returns:
            Querier: A instância atual da classe.
        """
        self.__whereIsNull(column, "AND", True)
        return self

    def __whereLike(self, column: str, value: str, operator: str):
        idx = len(self.wheres_cols)
        key_param = f"{column}_{idx}"

        op = operator if idx > 0 else ""
        query = f" {op} {column} LIKE %({key_param})s"

        self.wheres_cols.append(query)
        self.wheres_param.append({key_param: value})

    def whereLike(self, column: str, value: str) -> "Querier":
        """
        Adiciona cláusulas WHERE LIKE à consulta.

        Args:
            column (str): Nome da coluna.
            value (str): Valor para a cláusula LIKE.

        Returns:
            Querier: A instância atual da classe.
        """
        self.__whereLike(column, value, "AND")
        return self

    def orWhereLike(self, column: str, value: str) -> "Querier":
        """
        Adiciona cláusulas OR WHERE LIKE à consulta.

        Args:
            column (str): Nome da coluna.
            value (str): Valor para a cláusula LIKE.

        Returns:
            Querier: A instância atual da classe.
        """
        self.__whereLike(column, value, "OR")
        return self

    def __whereBetween(self, column: str, dat1: str, dat2: str, operator: str):
        idx = len(self.wheres_cols)
        idparam = len(self.wheres_param)

        key_param1 = f"{column}_{idx}{idparam}"
        self.wheres_param.append({key_param1: dat1})

        key_param2 = f"{column}_{idx}{idparam+1}"
        self.wheres_param.append({key_param2: dat2})

        op = operator if idx > 0 else ""
        query = f" {op} {column} BETWEEN %({key_param1})s AND %({key_param2})s"

        self.wheres_cols.append(query)

    def whereBetween(self, column: str, dat1: str, dat2: str) -> "Querier":
        """
        Adiciona cláusulas WHERE BETWEEN à consulta.

        Args:
            column (str): Nome da coluna.
            dat1 (str): Valor inicial para a cláusula BETWEEN.
            dat2 (str): Valor final para a cláusula BETWEEN.

        Returns:
            Querier: A instância atual da classe.
        """
        self.__whereBetween(column, dat1, dat2, "AND")
        return self

    def orWhereBetween(self, column: str, dat1: str, dat2: str) -> "Querier":
        """
        Adiciona cláusulas OR WHERE BETWEEN à consulta.

        Args:
            column (str): Nome da coluna.
            dat1 (str): Valor inicial para a cláusula BETWEEN.
            dat2 (str): Valor final para a cláusula BETWEEN.

        Returns:
            Querier: A instância atual da classe.
        """
        self.__whereBetween(column, dat1, dat2, "OR")
        return self

    def exists(self):
        """
        Verifica se existem registros nas condições especificadas.

        Returns:
            Querier: A instância atual da classe.
        """

        return self

    def limit(self, limit: int) -> "Querier":
        """
        Define o valor LIMIT para a consulta.

        Args:
            limit (int): Valor LIMIT.

        Returns:
            Querier: A instância atual da classe.
        """
        if isinstance(limit, int):
            idx = len(self.wheres_cols)
            key_param = f"limit_{limit}_{idx}"
            self.wheres_param.append({key_param: limit})

            self.limit_number = f"%({key_param})s"
            return self
        else:
            raise Exception(f"Limit '{limit}' is not int")

    def offset(self, offset: int) -> "Querier":
        """
        Define o valor OFFSET para a consulta.

        Args:
            offset (int): Valor OFFSET.

        Returns:
            Querier: A instância atual da classe.
        """
        if isinstance(offset, int):
            idx = len(self.wheres_cols)
            key_param = f"offset_{offset}_{idx}"
            self.wheres_param.append({key_param: offset})

            self.offset_number = f"%({key_param})s"
            return self

        else:
            raise Exception(f"Offset '{offset}' is not int")

    def groupBy(self, value: str | list[str]) -> "Querier":
        """
        Define o valor GROUP BY para a consulta.

        Args:
            value (str | list[str]): Coluna ou colunas para agrupamento.

        Returns:
            Querier: A instância atual da classe.
        """
        self.groupby = value if type(value) == str else ", ".join(value)
        return self

    def orderBy(self, value: str | list[str]) -> "Querier":
        """
        Define o valor ORDER BY para a consulta.

        Args:
            value (str | list[str]): Coluna ou colunas para ordenação.

        Returns:
            Querier: A instância atual da classe.
        """
        self.orderby = value if type(value) == str else ", ".join(value)
        return self

    def __get_data(self):

        if self.table_name is None:
            raise Exception("Table not configured")

        if self.columns == []:
            self.columns = ["*"]
            # raise Exception("Columns not configured")

        params_list = []
        query = f"SELECT * FROM {self.table_name}"

        for param_dict in self.wheres_param:
            params_list.append(param_dict)

        if self.wheres_cols:
            query += " WHERE"
            for query_where in self.wheres_cols:
                query += query_where

        if self.groupby:
            query += f" GROUP BY {self.groupby}"

        if self.orderby:
            query += f" ORDER BY {self.orderby}"

        if self.limit_number:
            query += f" LIMIT {self.limit_number}"

        if self.offset_number:
            query += f" OFFSET {self.offset_number}"

        params = dict(item for param_dict in params_list for item in param_dict.items())
        return query, params

    def get(self) -> list[dict]:
        """
        Executa a consulta SELECT e retorna todos os resultados.

        Returns:
            list[dict]: Uma lista de dicionários representando os resultados da consulta.
        """
        query, params = self.__get_data()

        data = self.conn.set_query(query=query, params=params).execute().fetch_all()
        return data

    def first(self) -> dict | None:
        """
        Executa a consulta SELECT e retorna o primeiro resultado.

        Returns:
            dict | None: Um dicionário representando o primeiro resultado da consulta ou None se não houver resultados.
        """

        query, params = self.__get_data()
        return self.conn.set_query(query=query, params=params).execute().fetch_one()

    def insert(self, values: dict | list[dict]) -> list[int]:
        """
        Executa a consulta INSERT com os valores especificados.

        Args:
            values (dict | list[dict]): Valores a serem inseridos. Pode ser um dicionário ou uma lista de dicionários.

        Returns:
            list[int]: Uma lista de IDs gerados no processo de inserção.
        """
        many = True
        if isinstance(values, dict):
            values = [values]
            many = False

        columns = list(values[0].keys())

        placeholders = ", ".join(["%s" for _ in range(len(columns))])
        query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders})"

        data = []
        for val in values:
            if set(columns) != set(val.keys()):
                raise ValueError("All records must have the same columns")
            data.append(list(val.values()))

        if not many:
            data = data[0]

        return self.conn.set_query(query, data).execute().insert(many)

    def update(self, values: dict) -> bool:
        """
        Executa a consulta UPDATE com os valores especificados.

        Args:
            values (dict): Valores a serem atualizados.

        Returns:
            bool: True se a atualização for bem-sucedida, False caso contrário.
        """
        columns = list(values.keys())
        placeholders = ", ".join([f"{column} = %({column})s" for column in columns])

        params_list = [values]
        query = f"UPDATE {self.table_name} SET {placeholders}"

        if self.wheres_cols:
            query += " WHERE"
            for param_dict in self.wheres_param:
                params_list.append(param_dict)

            for query_where in self.wheres_cols:
                query += query_where

        params = dict(item for param_dict in params_list for item in param_dict.items())
        return self.conn.set_query(query, params).execute().update()

    def delete(self) -> bool:
        """
        Executa a consulta DELETE com base nas condições especificadas.

        Returns:
            bool: True se a exclusão for bem-sucedida, False caso contrário.
        """
        params_list = []
        query = f"DELETE FROM {self.table_name}"

        if self.wheres_cols:
            query += " WHERE"
            for param_dict in self.wheres_param:
                params_list.append(param_dict)

            for query_where in self.wheres_cols:
                query += query_where

        params = dict(item for param_dict in params_list for item in param_dict.items())
        return self.conn.set_query(query, params).execute().delete()

    def toSql(self, formated: bool = True) -> str | dict:
        """
        Obtém a consulta SQL gerada com ou sem formatação.

        Args:
            formated (bool): Indica se a consulta SQL deve ser formatada.

        Returns:
            str | dict: A consulta SQL gerada, com ou sem formatação, dependendo do valor do argumento formated.
        """
        query, params = self.__get_data()

        if formated:
            query = query.replace("%(", "'").replace(")s", "'")
            for key in params.keys():
                query = query.replace(key, str(params[key]))

            return query

        else:

            return {"query": query, "params": params}

    def get_columns(self) -> list[dict]:
        """
        Obtém as colunas e seus tipos de dados para a tabela especificada.

        Returns:
            list[dict]: Uma lista de dicionários representando as colunas da tabela e seus tipos de dados.
        """
        database = self.conn.conn_pool._cnx_config["database"]
        query = f"""
            SELECT COLUMN_NAME, DATA_TYPE FROM information_schema.columns 
            WHERE TABLE_SCHEMA ='{database}' AND table_name = '{self.table_name}'
        """
        return self.conn.set_query(query=query).execute().fetch_all()

    def get_count_records(self) -> dict | None:
        """
        Obtém o total de registros na tabela.

        Returns:
            dict | None: Um dicionário contendo o total de registros na tabela ou None se houver um erro.
        """
        query = f"SELECT COUNT(*) AS total FROM {self.table_name}"
        return self.conn.set_query(query=query).execute().fetch_one()
