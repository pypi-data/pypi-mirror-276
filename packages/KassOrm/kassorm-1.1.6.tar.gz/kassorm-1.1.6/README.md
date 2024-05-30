# KassORM

Gerenciamento de migrations, modelos, seeders e gerador de query
<p>Criado com o intuito de abstratir toda uma modelagem de dados, de forma fácil. Sua criação é baseada na biblioteca Eloquent vista no Laravel, framework PHP. A principio, não há muitos ORMs para python que são intuitivos no uso, inicialemente, neste pacote, era utilizado o SqlAlchemy, mas seu uso e documentação são complicados, com uma curva grande para aprendizado, não desmerecendo ele, sabemos o quão robusto e estável está atualmente, mas precisavamos de algo mais direto e que entendessemos a fundo o uso.</p>


## Indice


[Migration](#migration)
-   [Criar e executar](#criar-e-executar)
-   [Configurando uma migration](#configurando-uma-migration)
-   [Lista de tipos de campos e outras ferramentas](#lista-de-tipos-de-campos-e-outras-ferramentas)
-   [Relacionamentos](#relacionamentos)

[Querier](#querier)
-   [Select](#select)
    -   [Where](#where)
    -   [Group e Order](#group-e-order)
-   [Insert](#insert)
-   [Update](#update)
-   [Delete](#delete)
-   [SoftDelete](#softdelete)


[Modelr](#modelr)
-   [Select](#select-1)
    -   [Where](#where-1)
    -   [Group e Order](#group-e-order-1)
    -   [Relacionamentos](#relacionamentos)
        -   [1 para 1](#1-para-1)
        -   [1 para N](#1-para-n)
        -   [N para N](#n-para-n)
-   [Insert](#insert-1)
-   [Update](#update-1)
-   [Delete](#delete-1)
-   [SoftDelete](#softdelete-1)


<!-- [Classe Seeder](#seeder) in dev -->



<br><br><br><br>

## Migration
Uso de migrations são importantes para manter o versionamento do banco de dados. Veja abaixo como utilizar.

### Criar e executar 
Utilize o metodo 'make_file_migration()' informando o nome,  diretório, nome da tabela e opcionalmente um comentário. O nome da migration tem como prefixos 'create_' e 'alter_', então gere o nome com eles para que as regras de cada tipo sejam setadas no arquivo gerado.

```
name_migration = "create_users"
dir_migration = "database"
table = "users"
comment = "criação da tabela de usuários"
Migration().make_file_migration(name_migration, dir_migration, table, comment)
````


Para executar as migrations informe apenas o local onde elas estão no método "migrate()", este comando também cria uma tabela ( _migrations_ ) para gerenciamento de qual migration já foi executada.

```
dir_migration = "database"
Migration().migrate(dir_migration)
```

### Drop
Para reiniciar o processo, fazendo o rollback das migrations, use o metodo 'drop_all_migrations()'

```
dir_migration = "database"
Migration().drop_all_migrations(dir_migration)
```


### Configurando uma migration
O arquivo gerado terá a seguinte aparência:

```

from KassOrm import Migration

class migrate(Migration): 
  
    __type__ = 'create'  
    __table__ = 'users'
    __comment__ = 'criação da tabela de usuários'
    
    def up(self):
        self.id().add()
        self.datetime('created_at').add()       
        
        
    def down(self): 
        self.dropTableIfExists()        
        
```
Um valor opcional  *__ conn __* pode ser passado na classe, para determinar qual conexão usar, essa conexão deverá estar configurada em *configs/database*. Não informando será usado a conexão padrão.

É aqui que será criado os campos da tabela e seus relacionamentos. o metodo up(), é executado quando a migration é executada para criar, nesse caso, uma tabela, o down(), é o metodo responsavel por fazer o inverso, no caso dropar a tabela.


### Lista de tipos de campos e outras propriedades:

```
# colunas
id()
string(name, qnt)
bigInteger(name)
bigIntegerUnisigned(name)
text(name)
enum(name, values)
integer(name,qnt)
datetime(name)


# propriedades para as colunas
foreign(table, key, local_key)
nullable()
unsigned()
comment(comment)
unique(columns,name)
current_timestamp()
update_timestamp()
addColumn()
dropColumn(name)
after(column)
first(column)
dropTableIfExists()
```


### Relacionamentos
Para relacionar duas tabelas, use foreign() como abaixo:
```
from KassOrm import Migration

class adresses(Migration): 
  
    __type__ = 'create'  
    __table__ = 'adress'
    __comment__ = 'contem endereços'

    def up(self):
        self.id().add()
        self.string('name').add()
        self.string('number).add()

    def down(self): 
        self.dropTableIfExists()    



class migrate(Migration): 
  
    __type__ = 'create'  
    __table__ = 'users'
    __comment__ = 'criação da tabela de usuários'
    
    def up(self):
        self.id().add()
        self.datetime('created_at').add()     
        self.unsignedBigInteger('adress_id').add()     

        self.foreign(table="adress", key="id", local_key="adress_id").add()
        
        
    def down(self): 
        self.dropTableIfExists()        
        
```




<br><br><br><br>
## Querier
Criador de querys para maior segurança e abstração de banco de dados.

 Querier() recebe como parametro o nome da conexão (Querier('api')) que estará configurado dentro das configurações, caso não seja informada, será usada a conexão padrão (default).

Instanciar a classe e informar a tabela:
```
query = Querier('api').table("users")
```
Agora poderá usar a var *query* para fazer diversas buscas e filtros na mesma tabela.

```
query.get()
# SELECT * FROM users

query.where({"name":"kass"}).get()
# SELECT * FROM users WHERE (name = "kass")
```




### Select
Selecionando os campos, caso o método select não for chamado, será sempre retornado todos os campos
```
query.select(["name","login"])
```

Selecionando os campos e pegando todos os dados, get() finaliza a query
```
query.select(["name","login"]).get()
```

Selecionando os campos e pegando somente o primeiro registro, first() finaliza a query
```
query.select(["name","login"]).first()
```

Retornando a query a executar, toSql() finaliza a query
```
query.select(["name","login"]).toSql()
```

Retornando a query separado dos parametros, toInfo() finaliza a query
```
query.select(["name","login"]).toInfo()
```

Limit e offset
```
query.limit(10).offset(2).get()
```

### Where
Para filtrar os dados podemos usar vários metodos encadeados.
```
query.where({"name":"admin,"id":1}).get()
# SELECT *  FROM users WHERE ( name = admin AND  id = 1 )

query.where({"name":"admin,"id":1}).orWhere({"id":2}).get()
# SELECT *  FROM users WHERE ( name = admin AND  id = 1 ) OR ( id = 2 )

query.whereIn("name",["admin","kass"]).get()
# SELECT * FROM users WHERE (name  IN ('admin', 'kass'))

query.whereIsNull("admin").get()
# SELECT *  FROM users WHERE ( admin IS  NULL )

query.whereIsNotNull("admin").get()
# SELECT *  FROM users WHERE ( admin IS NOT NULL )

query.whereLike("name","%kass%").get()
# SELECT *  FROM users WHERE ( name LIKE %kass% )

query.whereNotIn("name",["marcos","bee"]).get()
# SELECT *  FROM users WHERE (name NOT IN ('marcos', 'bee'))

```

### Group e Order
Para agrupar basta passar uma string com as colunas:
```
query.groupBy("name, login").get()
```
ou uma lista de colunas:
```
query.groupBy(["name","login"]).get()
```

Ordenação, pode-se passar uma string:
```
query.orderBy("name asc, login desc").get()
```

ou um dicionário informando a coluna e a direção:
```
query.orderBy({"name":"asc", "login":"desc"}).get()
```


### Insert
Insere um ou mais registros
```
Querier().table("users").insert({"name":"kass"})

Querier().table("users").insert([{"name":"kass"},{"name":"admin"}])
```


### Update
Atualizando um valor.
```
Querier().table("users").where({"id":1}).update({"name":"ADMINISTRADOR","login":"ADMIN"})
```

<p><b>
OBS: Não esqueça de sempre utilizar a clausula *where* quando for atualizar registros.
</b></p>

### Delete

Exclua um ou mais registros definitivamente
```
Querier().table("users").whereIn("id",[1,2]).delete()
```

### SoftDelete

Para trabalhar com softDelete, ou seja,  não deletar um registro e sim desativar, você somente precisará configurar a classe *Querier()* com o parametro *softDelete* e informar nele qual a coluna que representa a desativação do registro, essa coluna deverá ser do tipo *datetime*, geralmente a coluna se chama *deleted_at*.
```
Querier(softDelete="deleted_at").table("users").where({"id":1}).delete()
```
O registro é atualizado na coluna determinada com a data e hora do delete.


Com essa configuração o select será afetado, não retornando os registros em que o campo determinado não for nulo.
```
Querier(softDelete="deleted_at").table("users").get()
# retorna tudo menos o id 1 que esta 'deletado'
```

Para retornar tudo, inclusive o que foi deletado, use o método *withTrashed()*
```
Querier(softDelete="deleted_at").table("users").withTrashed().get()
```

Utilize o método *active()*, para ativar um registro anteriormente deletado com softDelete. Este método só tem efeito utilizando o *withTrashed()*.
```
Querier(softDelete="deleted_at").table("users").withTrashed().active()
```
<p><b>
OBS: Não esqueça de sempre utilizar a clausula *where* quando for excluir registros.
</b></p>









<br><br><br><br>

## Modelr
Classe para abstrair a classe Querier() e facilitar o uso dos dados nas tabelas, relacionamentos e informações sobre as queries de forma facilitada.


Veja a estrutura básica de um modelo:
```
from KassOrm import Modelr

class User(Modelr)

    __conn__ = 'api'
    __table__ = 'users'

```

Sendo que foi necessário fazer o import da classe Modelr e a injeção do mesmo no modelo. Duas configurações apra o modelo são: qual a conexão (__conn__) e qual a tabela do banco (__table__) que o model representa. Se não informar a conexão, ele irá pegar a conexaõ padrão (default) configurada.

### Select

Pegando todos os dados
```
User().get()
```

Pegando somente o primeiro registro
```
User().first()
```

Escolhendo colunas exibir
```
User().select(['name','login']).get()
```

Pegando todos os dados filtrados
```
User().where({"name":"admin,"id":1}).get()
```

Pegando sql e parametros
```
# exibe a query executada
User().where({"name":"admin,"id":1}).toSql()

# exibe a query e seus parametros separados
User().where({"name":"admin,"id":1}).toInfo()
```

Limit e offset
```
User().where({"name":"admin,"id":1}).limit(10).offset(2).get()
```

### Where
Para filtrar os dados podemos usar vários metodos encadeados.
```
User().where({"name":"admin,"id":1}).get()
# SELECT *  FROM users WHERE ( name = admin AND  id = 1 )

User().where({"name":"admin,"id":1}).orWhere({"id":2}).get()
# SELECT *  FROM users WHERE ( name = admin AND  id = 1 ) OR ( id = 2 )

User().whereIn("name",["admin","kass"]).get()
# SELECT * FROM users WHERE (name  IN ('admin', 'kass'))

User().whereIsNull("admin").get()
# SELECT *  FROM users WHERE ( admin IS  NULL )

User().whereIsNotNull("admin").get()
# SELECT *  FROM users WHERE ( admin IS NOT NULL )

User().whereLike("name","%kass%").get()
# SELECT *  FROM users WHERE ( name LIKE %kass% )

User().whereNotIn("name",["marcos","bee"]).get()
# SELECT *  FROM users WHERE (name NOT IN ('marcos', 'bee'))

```

<br>

#### Relacionamentos
### 1 para 1
Para montar seus relacionamentos, crie métodos dentro do seu modelo como abaixo.

Pensando que cada User (campo id) tem um Phone (campo user_id)  (1 para 1):
```
from KassOrm import Modelr

class Phone(Modelr)
    __conn__ = 'api'
    __table__ = 'phones'


class User(Modelr)
    __conn__ = 'api'
    __table__ = 'users'

    def phone(self):
        return self.hasOne(Phone, "user_id","id")

```

Usando o relacionamento.
```
User().related('phone').get()
```
O método *"related()"* recebe uma string ou uma lista de strings.


Retorno do relacionamento seria:
```
[
    {
        "id":1,
        "name":"admin",
        "phone":{
            "id":1,
            "user_id":1,
            "number":"12334567"
        }
    }
]
```
Onde a chave 'phone' representa os dados do relacionamento de User com Phone.

O método *"hasOne"* recebe os parametros: 
-   Phone => (model) modelo a se relacionar
-   user_id => (model_key) nome do campo dentro de Phone que representa o user
-   id => (local_key) identificador de User




<br>

### 1 para N
Agora vamos exemplificar que cada User tem muitos endereços (Address).

```
from KassOrm import Modelr

class Phone(Modelr)
    __conn__ = 'api'
    __table__ = 'phones'


class Address(Modelr)
    __conn__ = 'api'
    __table__ = 'addresses'


class User(Modelr)
    __conn__ = 'api'
    __table__ = 'users'

    def phone(self):
        return self.hasOne(Phone, "user_id","id")

    def addresses(self):
        return self.hasMany(Address, "user_id","id")        

```

Usando o relacionamento.
```
User().related(['phone','addresses']).get()
```

O método *"related()"* recebe uma string ou uma lista de strings.
Retorno dos relacionamentos seria:
```
[
    {
        "id":1,
        "name":"admin",
        "phone":{
            "id":1,
            "user_id":1,
            "number":"12334567"
        },
        "addresses":[
            {
                "id":1,
                "user_id:1,
                "address":"RUA 1"
            },
            {
                "id":2,
                "user_id:1,
                "address":"RUA 2"
            },
        ]
    }
]
```
Onde a chave 'addresses' representa os dados do relacionamento de User com Address.

O método *"hasMany"* recebe os parametros: 
-   Address => (model) modelo a se relacionar
-   user_id => (model_key) nome do campo dentro de Address que representa o user
-   id => (local_key) identificador de User

<br>


### N para N
Para casos que há muitos para muitos, devemos usar uma tabela intermediária. Segue como deria um relacionamento de User com Permission (permissões).

```
from KassOrm import Modelr

class Phone(Modelr)
    __conn__ = 'api'
    __table__ = 'phones'


class Address(Modelr)
    __conn__ = 'api'
    __table__ = 'addresses'


class Permission(Modelr)
    __conn__ = 'api'
    __table__ = 'permissions'    


class User(Modelr)
    __conn__ = 'api'
    __table__ = 'users'

    def phone(self):
        return self.hasOne(Phone, "user_id","id")

    def addresses(self):
        return self.hasMany(Address, "user_id","id")   

    def permissions(self):
        return self.hasManyToMany(Permission, 'id', 'permission_id', 'users_apps_permissions', 'user_id', 'id')                

```


Usando o relacionamento.
```
User().related(['phone','addresses','permissions']).get()
```
O método *"related()"* recebe uma string ou uma lista de strings.


Retorno dos relacionamentos seria:
```
[
    {
        "id":1,
        "name":"admin",
        "phone":{
            "id":1,
            "user_id":1,
            "number":"12334567"
        },
        "addresses":[
            {
                "id":1,
                "user_id:1,
                "address":"RUA 1"
            },
            {
                "id":2,
                "user_id:1,
                "address":"RUA 2"
            },
        ],
        "permissions":[
            {
                "id":1,
                "name":"acesso geral"
            },            
            {
                "id":2,
                "name":"acesso a cadastrar"
            },
            {
                "id":3,
                "name":"acesso a excluir"
            }
        ]
    }
]
```
Onde a chave 'permissions' representa os dados do relacionamento de User com Permission.

O método *"hasManyToMany"* recebe os parametros: 
-   Permission => (model) modelo a se relacionar
-   id => (model_key) identificador de Permission
-   permission_id => (intermediate_model_key) identificador de Permission na tabela intermediária
-   users_apps_permissions => (intermediate_table) nome da tabela intermediária
-   user_id => (intermediate_local_key) identificador de User na tabela intermediária
-   id => (local_key)  identificador de User


#### Pegando dados da tabela intermediária
O metodo *"hasManyToMany"* ainda pode receber o encadeamento de *"withPivot()"*, que pode receber uma lista de nomes dos campos a exibir da tabela intermediária, se não for passado a lista, será retornado todos os campos da tabela intermediária. Veja o exemplo:


```
from KassOrm import Modelr

.
.
.

class User(Modelr)
    __conn__ = 'api'
    __table__ = 'users'

    def phone(self):
        return self.hasOne(Phone, "user_id","id")

    def addresses(self):
        return self.hasMany(Address, "user_id","id")   

    def permissions(self):
        return self.hasManyToMany(Permission, 'id', 'permission_id', 'users_apps_permissions', 'user_id', 'id')->withPivot()                

```
Alterando o retorno da chave permissions para:
```
[
    {
        .
        .
        .
        "permissions":[
            {
                "id":1,
                "name":"acesso geral",
                "pivot":{
                    "user_id":1,
                    "permission_id":1,
                }
            },            
            {
                "id":2,
                "name":"acesso a cadastrar",
                "pivot":{
                    "user_id":1,
                    "permission_id":2,
                }
            },
            {
                "id":3,
                "name":"acesso a excluir",
                "pivot":{
                    "user_id":1,
                    "permission_id":3,
                }
            }
        ]
    }
]
```

Passando, *"->withPivot(["user_id"])"*, somente o campo user_id seria exibido

### Group e Order
Para agrupar basta passar uma string com as colunas:
```
User().groupBy("name, login").get()
```
ou uma lista de colunas:
```
User().groupBy(["name","login"]).get()
```

Ordenação, pode-se passar uma string:
```
User().orderBy("name asc, login desc").get()
```

ou um dicionário informando a coluna e a direção:
```
User().orderBy({"name":"asc", "login":"desc"}).get()
```

### Insert


```
id = User().insert({"name":"kass"})
print(id)

ids = User().insert([{"name":"admin"},{"name":"kass"}])
print(ids)
```


### Update
Atualizando um registro.
```
User().where({"id":1}).update({"name":"admin"})
```
<p><b>
OBS: Não esqueça de sempre utilizar a clausula *where* quando for atualizar registros.
</b></p>


### Delete
Para excluir um registro utilize o método delete().
```
User().where({"id":1}).delete()
```

### SoftDelete

Para trabalhar com softDelete, ou seja,  não deletar um registro e sim desativar, você somente precisará configurar o seu model com a constante  *__sofDelete__* e informar nele qual a coluna que representa a desativação do registro, essa coluna deverá ser do tipo *datetime*, geralmente a coluna se chama *deleted_at*.
```
class User(Modelr):    
   
    __sofDelete__="deleted_at"
```

para excluir use normal o metodo delete.
```
User().where({"id":1}).delete()
```
O registro é atualizado na coluna determinada com a data e hora do delete.



Com essa configuração o select será afetado, não retornando os registros em que o campo determinado não for nulo.
```
User().get()
# retorna tudo menos o registro que esta 'deletado'
```

Para retornar tudo, inclusive o que foi deletado, use o método *withTrashed()*
```
User().withTrashed().get()
```

Utilize o método *active()*, para ativar um registro anteriormente deletado com softDelete. Este método só terá efeito utilizando o *withTrashed()*.
```
User().where({"id":1}).withTrashed().active()
```
<p><b>
OBS: Não esqueça de sempre utilizar a clausula *where* quando for excluir registros.
</b></p>




