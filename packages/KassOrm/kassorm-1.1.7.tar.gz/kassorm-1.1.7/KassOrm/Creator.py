import os
from pathlib import Path
from datetime import datetime as dt
from rich.console import Console


class Creator:

    console = Console()

    @staticmethod
    def getStub(name: str):
        """Pega um arquivo stub e retorna se conteudo

        Args:
            name (str): nome do arquivo stub

        Returns:
            str: conteudo do arquivo
        """

        dir = os.path.dirname(__file__)

        stub = open(Path(f"{dir}/stubs/{name}"), "r+")
        stub_content = stub.read()
        stub.close()

        return stub_content

    @staticmethod
    def make_migration(dir: str, migration_name: str, comment: str = ""):
        """Cria um arquivo de migração de acordo com o modelo pré estabelecido

        Args:
            dir (str): caminho ate o diretório das migrations
            migration_name (str): nome do arquivo
            comment (str, optional): um comentario sobre essa migration. Defaults to "".

        Returns:
            bool: retorna true ou false em caso de sucesso ou falha
        """

        if os.path.isdir(dir) == False:
            os.makedirs(dir)

        if "create_" in migration_name.lower():
            content = Creator.getStub("migration_create.stub")
            table = migration_name.lower().split("_", 1)[1]
        else:
            content = Creator.getStub("migration_alter.stub")
            table = migration_name.lower().replace("alter_", "")

        content = content.replace(
            "%COMMENT%", f"'{comment.lower()}'" if comment != "" else "''"
        )
        content = content.replace("%TABLE%", table)

        filename = dt.now().strftime("%Y_%m_%d__%H%M%S") + "_" + migration_name + ".py"
        file = open(f"{dir}/{filename}", "w+", encoding="utf-8")
        file.writelines(content)
        file.close()

        if os.path.isfile(f"{dir}/{filename}"):
            Creator.console.print(f"Migration '{filename}' created [OK]", style="green")
            return True

        Creator.console.print(f"Migration '{filename}' not created [FAIL]", style="red")
        return False

    @staticmethod
    def make_model(dir: str, model_name: str):
        """Cria um arquivo de model de acordo com o modelo pré estabelecido

        Args:
            dir (str): diretório dos modelos
            model_name (str): nome do modelo

        Raises:
            Exception: Caso o model já exista

        Returns:
            bool: retorna true ou false em caso de sucesso ou falha
        """

        if os.path.isdir(dir) == False:
            os.makedirs(dir)

        filename = model_name + ".py"

        if os.path.isfile(f"{dir}/{filename}"):
            raise Exception(f"Model '{model_name}' already exists")

        content = Creator.getStub("model.stub")

        content = content.replace("%MODELNAME%", model_name)

        file = open(f"{dir}/{filename}", "w+", encoding="utf-8")
        file.writelines(content)
        file.close()

        if os.path.isfile(f"{dir}/{filename}"):
            Creator.console.print(f"Model '{filename}' created [OK]", style="green")
            return True

        Creator.console.print(f"Model '{filename}' not created [FAIL]", style="red")
        return False

    @staticmethod
    def make_seeder():
        Creator.console.print(f"Seeder command in dev", style="yellow")

    @staticmethod
    def make_factory():
        Creator.console.print(f"Factory command in dev", style="yellow")
