import os
import glob
import importlib
import logging
import traceback
from pathlib import Path
from KassOrm.Conn import Conn
from rich.console import Console


class Properties:

    def __init__(self) -> None:
        self.columns = []

    def id(self):
        """Coluna chamada 'ID' do tipo BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY"""
        col = "id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY"
        self.columns.append(col)
        return

    def string(self, name: str, qnt: int = 255):
        """Coluna do tipo 'VARCHAR'

        Args:
            name (str): nome da coluna
            qnt (int, optional): quantidade de caracteres aceitos. Defaults to 255.

        Returns:
            _type_: _description_
        """
        col = "{} VARCHAR({}) NOT NULL ".format(name, qnt)
        self.columns.append(col)
        return self

    def bigInteger(self, name: str):
        """Coluna do tipo 'BIGINT'

        Args:
            name (str): nome da coluna
        """
        col = "{} BIGINT NOT NULL".format(name)
        self.columns.append(col)
        return self

    def bigIntegerUnsigned(self, name: str):
        """Coluna do tipo 'BIGINT UNSIGNE'

        Args:
            name (str): nome da coluna
        """
        col = "{} BIGINT UNSIGNED NOT NULL".format(name)
        self.columns.append(col)
        return self

    def text(self, name: str):
        """Coluna do tipo 'TEXT'

        Args:
            name (str): nome da coluna
        """
        col = "{} TEXT NOT NULL".format(name)
        self.columns.append(col)
        return self

    def enum(self, name: str, values: list):
        """Coluna do tipo 'ENUM'

        Args:
            name (str): nome da coluna
            values (list[str]): lista de str com valores aceitos
        """
        str_values = ", ".join(map(lambda x: f'"{x}"', values))
        col = "{} ENUM({}) NOT NULL".format(name, str_values)
        self.columns.append(col)
        return self

    def integer(self, name: str, qnt: int = None):
        """Coluna do tipo 'INT'

        Args:
            name (str): nome da coluna
            qnt (int, optional): quantidade de caracteres aceito. Defaults to None.
        """
        if qnt != None:
            col = "{} INT({}) ZEROFILL UNSIGNED NOT NULL".format(name, qnt)
        else:
            col = "{} INT NOT NULL".format(name)

        self.columns.append(col)
        return self

    def datetime(self, name: str):
        """Coluna do tipo 'DATETIME'

        Args:
            name (str): nome da coluna
        """
        col = "{} DATETIME NOT NULL".format(name)
        self.columns.append(col)
        return self

    def date(self, name: str):
        col = "{} DATE NOT NULL ".format(name)
        self.columns.append(col)
        return self

    def longtext(self, name: str):
        col = "{} LONGTEXT NOT NULL ".format(name)
        self.columns.append(col)
        return self

    def mediumtext(self, name: str):
        col = "{} MEDIUMTEXT NOT NULL ".format(name)
        self.columns.append(col)
        return self

    def decimal(self, name: str):
        col = "{} DECIMAL NOT NULL ".format(name)
        self.columns.append(col)
        return self

    def float(self, name: str):
        col = "{} FLOAT NOT NULL ".format(name)
        self.columns.append(col)
        return self

    def default(self, value: str):
        """Propriedade 'DEFAULT' da coluna definindo qual o valor padrão

        Args:
            value (str): valor padrão da coluna
        """
        if self.columns:
            last_column = self.columns[-1]

            if value.lower() == "null":
                last_column += " DEFAULT NULL"
            else:
                last_column += " DEFAULT '{}'".format(value)
            self.columns[-1] = last_column
        return self

    def unsigned(self):
        """Propriedade 'UNSIGNED' da coluna definindo que só aceita valores positivos

        Returns:
            _type_: _description_
        """
        if self.columns:
            last_column = self.columns[-1]
            last_column += " UNSIGNED"
            self.columns[-1] = last_column
        return self

    def nullable(self):
        """Propriedade 'NULL' da coluna definindo aceita valores nulos"""
        if self.columns:
            last_column = self.columns[-1]
            last_column = last_column.replace("NOT NULL", "NULL")
            self.columns[-1] = last_column
        return self

    def comment(self, comment: str):
        """Propriedade 'COMMENT' da coluna definindo um comentário"""
        if self.columns:
            last_column = self.columns[-1]
            last_column += " COMMENT '{}'".format(comment)
            self.columns[-1] = last_column
        return self

    def unique(self, columns: list = None, name: str = None):
        """Propriedade ou método para gerar valores unicos em um coluna ou em um conjunto

        Args:
            columns (list, optional): lista das colunas a serem agrupadas como unicas. Defaults to None.
            name (str, optional): nome do incide unico. Defaults to None.

        Returns:
            _type_: _description_
        """
        if columns != None and name != None:
            uniq = ""
            for col in columns:
                uniq += f"{col}, "
            uniq = uniq[:-2]

            col = " UNIQUE KEY {} ({})".format(name, uniq)
            self.columns.append(col)
            return
        else:
            if self.columns:
                last_column = self.columns[-1]
                last_column += f" UNIQUE"
                self.columns[-1] = last_column
            return self

    def current_timestamp(self):
        """Propriedade para campos de timestamp definindo que devem inserir a hora atual ao inserir um registro"""
        if self.columns:
            last_column = self.columns[-1]
            last_column += " DEFAULT CURRENT_TIMESTAMP"
            self.columns[-1] = last_column
        return self

    def update_timestamp(self):
        """Propriedade para campos de timestamp definindo que devem inserir a hora atual ao inserir um registro e atualiza caso o registro seja alterado"""
        if self.columns:
            last_column = self.columns[-1]
            last_column += " ON UPDATE CURRENT_TIMESTAMP"
            self.columns[-1] = last_column
        return self

    def foreign(self, col_local: str):
        """Metodo para gerar um relacionamento entre tabelas

        Args:
            col_local (str): coluna local da migration
        """

        if self.__type__ == "create":
            col = "FOREIGN KEY ({})".format(col_local)
        else:
            col = "ALTER TABLE {} ADD FOREIGN KEY ({})".format(
                self.__table__, col_local
            )
        self.columns.append(col)
        return self

    def references(self, table: str):
        """Metodo encadeado do foreign que seleciona qual a tabela a ser relacionada

        Args:
            table (str): nome da tabela
        """
        if self.columns:
            last_column = self.columns[-1]
            last_column += f" REFERENCES {table}".format(table)
            self.columns[-1] = last_column
        return self

    def on(self, col: str):
        """Metodo encadeado do references que indica qual a coluna na tabela relacionada

        Args:
            col (str): nome da coluna
        """
        if self.columns:
            last_column = self.columns[-1]
            last_column += " ({})".format(col)
            self.columns[-1] = last_column
        return self

    def add_column(self):
        if self.columns:
            last_column = self.columns[-1]
            last_column = (
                "ALTER TABLE {} ADD COLUMN ".format(self.__table__) + last_column
            )
            self.columns[-1] = last_column
        return self

    def first(self):
        if self.columns:
            last_column = self.columns[-1]
            last_column += f" FIRST"
            self.columns[-1] = last_column
        return self

    def after(self, col_existing: str):
        if self.columns:
            last_column = self.columns[-1]
            last_column += f" AFTER {col_existing}"
            self.columns[-1] = last_column
        return self

    def drop_table(self):
        """Gera a query para dropar uma tabela existente

        Args:
            table (str): nome da tabela
        """
        col = "DROP TABLE IF EXISTS {}".format(self.__table__)
        self.columns.append(col)
        return

    def drop_column(self, col: str):
        col = "ALTER TABLE {} DROP COLUMN {}".format(self.__table__, col)
        self.columns.append(col)
        return

    def drop_index(self, name: str):
        col = "DROP INDEX {} ON {}".format(name, self.__table__)
        self.columns.append(col)

    def add_index(self, name: str, columns: list[str], unique: bool = False):
        if isinstance(columns, str):
            columns = [columns]

        if unique:
            col = "CREATE UNIQUE INDEX {} ON {} ({})".format(
                name, self.__table__, ", ".join(columns)
            )
        else:
            col = "CREATE INDEX {} ON {} ({})".format(
                name, self.__table__, ", ".join(columns)
            )
        self.columns.append(col)
        return


class Migrater:

    def __init__(self, conn: dict, dir_migrations: str) -> None:

        self.console = Console()
        self.__setup_logging()

        self.__rollback__ = False
        self.__conn = conn
        self.__steps = None

        self.migrations = glob.glob(os.path.join(dir_migrations, "*.py"))
        self.dir_module = str(dir_migrations).replace("\\", ".").replace("/", ".")

    def __setup_logging(self) -> None:
        logging.basicConfig(
            filename="logs/KassOrm.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - Migrate() -%(message)s",
        )

    def execute(self, is_fresh_migrate: bool = False) -> bool:
        """Executa as migrações de um diretório.

        Args:
            fresh (bool): Se True, realiza uma recriação completa do banco de dados.

        Returns:
            bool: True se a execução for bem-sucedida.
        """
        self.__create_table_migrations()

        migration_rounds = (
            self.__execute_fresh_migrations()
            if is_fresh_migrate
            else self.__execute_normal_migrations()
        )

        for migration_round in migration_rounds:
            if migration_round > 0:
                self.__rollback__ = False
                self.migrations.reverse()

            if self.__rollback__ == False:

                for migration_file in self.migrations:
                    migration_path = Path(migration_file)
                    migration_name = migration_path.stem

                    if not self.__has_migration_saved(migration_name):
                        migration_instance, result = self.__up_or_down(migration_path)
                        if result:
                            self.__save_migration_executed(
                                migration_name, migration_instance.__comment__
                            )
            else:
                for index, migration_file in enumerate(self.migrations):
                    if isinstance(self.__steps, int):
                        if index >= self.__steps:
                            break
                    if isinstance(self.__steps, str):
                        if self.__steps == Path(migration_file).stem:
                            break

                    migration_path = Path(migration_file)
                    migration_name = migration_path.stem

                    if self.__has_migration_saved(migration_name):
                        migration_instance, result = self.__up_or_down(migration_path)
                        if result:
                            self.__delete_migration_executed(migration_name)
                        else:
                            if self.__steps != None:
                                self.__steps += 1

        return True

    def __execute_fresh_migrations(self) -> int:
        rounds = range(2)
        self.rollback()
        self.console.print("Freshing migrations", style="yellow")
        return rounds

    def __execute_normal_migrations(self) -> int:
        rounds = range(1)
        if self.__rollback__:
            self.console.print("Rolling back migrations", style="yellow")
        else:
            self.console.print("Executing migrations", style="yellow")

        return rounds

    def rollback(self, steps: int | str = None) -> bool:
        """Reverte um número específico de migrações.

        Args:
            steps (int): Número de migrações a reverter.
        """
        self.__rollback__ = True
        self.__steps = steps
        self.migrations.reverse()
        return self

    def __up_or_down(self, migration: str) -> tuple["Migrater", bool]:
        """Determina se a execução da migtation é para acrescentar (up) ou retirar (down) items de uma tabela

        Args:
            migration (str): nome da migration

        Returns:
            Migration, str: instância de Migration e a query a ser executada
        """
        migration_file = os.path.basename(migration).replace(".py", "")
        mod_file = self.dir_module + "." + migration_file

        module = importlib.import_module(mod_file)
        instance_migration = module.migrate()

        if self.__rollback__:
            instance = instance_migration.down()
            return instance, self.__query_down(instance)
        else:
            instance = instance_migration.up()
            return instance, self.__query_up(instance)

    def __query_down(self, Migration: "Migration") -> bool:
        """Gera a query para retirada de itens da tabela/banco de dados

        Args:
            Migration (Migration): instância da classe Migration

        Returns:
            str: query
        """
        res = False
        if Migration.__type__ == "create":

            if (
                Migration.columns[0].startswith("DROP")
                or Migration.columns[0].startswith("CREATE")
                or Migration.columns[0].startswith("ALTER")
            ):
                query = ", ".join(Migration.columns)
                res = Conn(self.__conn).set_query(query).execute().exec()
                if not res:
                    self.console.print(
                        f"Error in query execution: {query}", style="red"
                    )
                    return
            else:
                query = "ALTER TABLE {} ".format(Migration.__table__) + ", ".join(
                    Migration.columns
                )
                res = Conn(self.__conn).set_query(query).execute().exec()
                if not res:
                    self.console.print("Migration {} execution [FAIL]", style="red")
                    error_traceback = traceback.format_exc()
                    self.console.print(
                        f"Error in query execution: {error_traceback}", style="red"
                    )
                    return

        else:
            for query in Migration.columns:
                res = Conn(self.__conn).set_query(query).execute().exec()
                if res != True:
                    self.console.print(res, style="red")
                    return

        return res

    def __query_up(self, Migration: "Migration") -> bool:
        """Gera a query para adição de itens da tabela/banco de dados

        Args:
            Migration (Migration): instância da classe Migration

        Returns:
            str: query
        """

        if Migration.__type__ == "create":
            query = "CREATE TABLE IF NOT EXISTS {}"
            query = (
                query.format(Migration.__table__)
                + " ("
                + ", ".join(Migration.columns)
                + ")"
            )
            res = Conn(self.__conn).set_query(query).execute().exec()
            if res != True:
                self.console.print("Migration not executed [FAIL]", style="red")
                raise Exception(f"Error in query execution: {query}")
        else:
            for query in Migration.columns:
                res = Conn(self.__conn).set_query(query).execute().exec()
                if res != True:
                    self.console.print("Migration not executed [FAIL]", style="red")
                    raise Exception(res)

        return True

    def __create_table_migrations(self) -> bool:
        """Cria a tabela parametro das migrations executadas"""
        query = """
                CREATE table if not exists _migrations_ (
                    id BIGINT unsigned not null auto_increment,
                    date DATETIME not null,
                    migration VARCHAR(255) not null unique,
                    description VARCHAR(255) null,
                    PRIMARY KEY (`id`)
                );
            """
        return Conn(self.__conn).set_query(query).execute().create()

    def __truncate_table_migrations(self) -> bool:
        query = "TRUNCATE _migrations_"
        return Conn(self.__conn).set_query(query).execute().drop()

    def __has_migration_saved(self, migration_name: str) -> bool:
        """Verifica se há registro de execução de uma migration

        Args:
            migration_name (str): nome do arquivo da migration

        Returns:
            bool: se obteve sucesso ou falha
        """

        query = "SELECT * FROM _migrations_ WHERE migration = %(migration)s"
        data = (
            Conn(self.__conn)
            .set_query(query, {"migration": migration_name})
            .execute()
            .fetch_one()
        )

        if data == None:
            return False

        self.console.print(f"Migration {migration_name} [EXISTS] ")
        return True

    def __save_migration_executed(
        self, migration_name: str, description: str = ""
    ) -> bool:
        """Salva uma migration no banco para posterior verificação

        Args:
            migration_name (str): nome do arquivo da migration
            description (str): descrição informada na migration na prop __comment__

        Returns:
            bool: se obteve sucesso ou falha
        """
        if self.__rollback__ == False:
            query = """INSERT INTO _migrations_ (date, migration, description) VALUES (NOW(), %(migration)s, %(description)s)"""
            res = (
                Conn(self.__conn)
                .set_query(
                    query, {"migration": migration_name, "description": description}
                )
                .execute()
                .insert()
            )

            if res:
                self.console.print(
                    f"Migration {migration_name} executed [OK]", style="green"
                )

        return res

    def __delete_migration_executed(self, migration_name: str) -> bool:
        if self.__rollback__ == True:
            query = "DELETE FROM _migrations_ WHERE migration = %(migration)s"
            res = (
                Conn(self.__conn)
                .set_query(query, {"migration": migration_name})
                .execute()
                .delete()
            )
        if res:
            self.console.print(
                f"Migration {migration_name} dropped [OK]", style="yellow"
            )

        return res


class Migration(Properties):

    __type__ = None
    __table__ = None
    __comment__ = None
    __connection__ = None

    def __init__(self) -> None:
        self.columns = []

    def up(self):
        """Metodo de adição de itens no banco"""
        return self

    def down(self):
        """Metodo para retirarda de itens no banco"""
        return self
