import json
import os
import inspect
from datetime import date
from datetime import datetime as dt
from .Querier import Querier


class HasManyOfMany:
    def run(self): ...


class HasOneMany:
    def run(self, rows: list, __has: dict):
        ids = []
        for row in rows:
            ids.append(str(row[__has["local_key"]]))

        if inspect.ismodule(__has["model"]):
            class_name = os.path.basename(str(__has["model"])).replace(".py'>", "")
            instaceModel = getattr(__has["model"], class_name)
        else:
            instaceModel = __has["model"]

        related_rows = instaceModel().whereIn(__has["model_key"], ids).get()

        return rows, __has, related_rows


class HasMany:

    def run(self, rows: list, __has: dict):
        rows, __has, related_rows = HasOneMany().run(rows, __has)

        for row in rows:
            row[__has["related_name"]] = []
            for row2 in related_rows:
                if row[__has["local_key"]] == row2[__has["model_key"]]:
                    row[__has["related_name"]].append(row2)

        return rows


class HasOne:
    def run(self, rows: list, __has: dict):
        rows, __has, related_rows = HasOneMany().run(rows, __has)

        for row in rows:
            row[__has["related_name"]] = {}
            if related_rows is not None:
                for row2 in related_rows:
                    if row[__has["local_key"]] == row2[__has["model_key"]]:
                        row[__has["related_name"]] = row2

        return rows


class Modelr:

    __conn__ = None
    __table__ = None
    __softdelete__ = None

    def __init__(self) -> None:
        self.querier = Querier(conn=self.__conn__).table(self.__table__)
        self.withtrashed = False

        self.relashionships = []
        self.__has = {}
        self.columns = None

    def withTrashed(self):
        self.withtrashed = True
        return self

    def __with_trash(self):
        if self.__softdelete__ is not None and self.withtrashed == False:
            return True
        else:
            return False

    def select(self, cols: str | list[str] = "*"):
        # self.querier.select(cols)
        self.columns = cols
        return self

    def where(self, conditional: list[dict] | dict):
        self.querier.where(conditional)
        return self

    def orWhere(self, conditional: list[dict] | dict):
        self.querier.orWhere(conditional)
        return self

    def whereIn(self, column: str, values: list[str]):
        self.querier.whereIn(column, values)
        return self

    def orWhereIn(self, column: str, values: list[str]):
        self.querier.orWhereIn(column, values)
        return self

    def whereNotIn(self, column: str, values: list[str]):
        self.querier.whereNotIn(column, values)
        return self

    def orWhereNotIn(self, column: str, values: list[str]):
        self.querier.orWhereNotIn(column, values)
        return self

    def whereIsNull(self, column: str):
        self.querier.whereIsNull(column)
        return self

    def orWhereIsNull(self, column: str):
        self.querier.orWhereIsNull(column)
        return self

    def whereIsNotNull(self, column: str):
        self.querier.whereIsNotNull(column)
        return self

    def orWhereIsNotNull(self, column: str):
        self.querier.orWhereIsNotNull(column)
        return self

    def whereLike(self, column: str, value: str):
        self.querier.whereLike(column, value)
        return self

    def orWhereLike(self, column: str, value: str):
        self.querier.orWhereLike(column, value)
        return self

    def whereBetween(self, column: str, dat1: str, dat2: str):
        self.querier.whereBetween(column, dat1, dat2)
        return self

    def orWhereBetween(self, column: str, dat1: str, dat2: str):
        self.querier.orWhereBetween(column, dat1, dat2)
        return self

    def limit(self, limit: int):
        self.querier.limit(limit)
        return self

    def offset(self, offset: int):
        self.querier.offset(offset)
        return self

    def groupBy(self, value: str | list[str]):
        self.querier.groupBy(value)
        return self

    def orderBy(self, value: str | list[str]):
        self.querier.orderBy(value)
        return self

    def json_date_serializer(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()

    def get(self):
        if self.__with_trash():
            self.querier.whereIsNull(self.__softdelete__)

        rows = self.querier.get()

        if len(rows) == 0:
            rows = None

        if self.relashionships and rows is not None:

            for has in self.relashionships:
                if has["related_type"] == "HasMany":
                    rows = HasMany().run(rows, has)
                elif has["related_type"] == "HasOne":
                    rows = HasOne().run(rows, has)

        if self.columns is not None:
            new_rows = []
            for dicionario in rows:
                new_dict = {
                    chave: valor
                    for chave, valor in dicionario.items()
                    if chave in self.columns
                }
                new_rows.append(new_dict)
            rows = new_rows

        rows = json.dumps(rows, default=self.json_date_serializer)
        return json.loads(rows)

    def first(self):
        if self.__with_trash():
            self.querier.whereIsNull(self.__softdelete__)

        rows = self.querier.first()

        if self.relashionships and rows is not None:

            rows = [rows]

            for has in self.relashionships:
                if has["related_type"] == "HasMany":
                    rows = HasMany().run(rows, has)
                elif has["related_type"] == "HasOne":
                    rows = HasOne().run(rows, has)

        if self.columns is not None:
            new_rows = []
            for dicionario in rows:
                new_dict = {
                    chave: valor
                    for chave, valor in dicionario.items()
                    if chave in self.columns
                }
                new_rows.append(new_dict)
            rows = new_rows[0]

        rows = json.dumps(rows, default=self.json_date_serializer)
        rows = json.loads(rows)

        if type(rows) == dict:
            return rows
        else:
            return rows[0]

    def toSql(self, formmated: bool = True):
        return self.querier.toSql(formmated)

    def delete(self):
        if self.__with_trash():
            return self.querier.update({self.__softdelete__: dt.now()})
        return self.querier.delete()

    def active(self):
        if self.__with_trash():
            return self.querier.update({self.__softdelete__: None})

    def update(self, values: dict):
        if self.__softdelete__ is not None:
            self.querier.whereIsNull(self.__softdelete__)

        return self.querier.update(values)

    def insert(self, values: dict | list[dict]):
        return self.querier.insert(values)

    def withRelated(self, relateds: str | list[str]):

        def getRelated(d):
            method = getattr(self, d)
            method()

        if type(relateds) == str:
            getRelated(relateds)
            self.__has["related_name"] = relateds
            self.relashionships.append(self.__has)
        else:
            for i in relateds:
                self.__has = {}
                getRelated(i)
                self.__has["related_name"] = i
                self.relashionships.append(self.__has)

        return self

    def hasManyOfmany(
        self,
        model: "Modelr",
        model_key: str,
        pivot_model_key: str,
        pivot_table: str,
        pivot_local_key: str,
        local_key: str,
    ):
        self.__has["related_type"] = "HasMany"

        self.__has["model"] = model
        self.__has["model_key"] = model_key
        self.__has["pivot_model_key"] = pivot_model_key
        self.__has["pivot_table"] = pivot_table
        self.__has["pivot_local_key"] = pivot_local_key
        self.__has["local_key"] = local_key

    def hasMany(self, model: "Modelr", model_key: str, local_key: str):
        self.__has["related_type"] = "HasMany"

        self.__has["model"] = model
        self.__has["model_key"] = model_key
        self.__has["local_key"] = local_key

    def hasOne(self, model: "Modelr", model_key: str, local_key: str):
        self.__has["related_type"] = "HasOne"

        self.__has["model"] = model
        self.__has["model_key"] = model_key
        self.__has["local_key"] = local_key
