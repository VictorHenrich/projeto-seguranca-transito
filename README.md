# Documentação API - Segurança no trânsito

<br>
<br>

## Descrição

Este projeto tem como foco o desenvolvimento de uma aplicação web com intuito de facilitar, auxiliar e gerenciar acidentes que acontecem todos os dias em nosso trânsito. Inicialmente este projeto terá como foco principal auxiliar pessoas que acabaram de sofrer um acidente, muitas vezes delas ficam desatentas a certos requisitos necessários  / importantes para uma esta situação, como por exemplo conseguir identificar sua localização, colocar sinalizações, etc...

Para atender as expectativas do projeto será desenvolvido um aplicativo *mobile* que será utilizado pela pessoa, ali será mostrado um guia do que se deve fazer em cada situação como também terá um suporte de conexão direta com a central, que é a responsável por gerenciar os usuários e assim solicitar atendimento as autoridades competentes caso necessário.

Por outra ponta será desenvolvido um sistema web acessado pelo navegador para o gerenciamento desses acidentes, como os usuários cadastraram com suas informações pessoais será utilizado elas para identificação, também terá sua localização compartilhada  através do gps no celular. Tudo isso será nencessário para agilizar os processos que envolvem chamadas.

<br>
<br>
<br>

## Autenticação

Cada tipo de usuários existentes no sistema terá sua própria rota, afim de ogrnização. Qualquer um dos casos será retornado um *hash* do tipo Bearer

Nesta API será possível realizar dois tipos de autenticação:

* **Usuário Comum**
* **Usuário dos Departamentos**

<br>
<br>
<br>
<br>
<br>
<br>

> ## (POST) /autenticacao/usuario


Nesta autenticação o usuário será necessario inserir seu email e senha de cadastro, caso não possuir deverá se registrar ao sistema para conseguir logar.
<br>
<br>

### HEADER

* **Content-Type: application/json**

<br>

### BODY
<br>

| Campo | Tipo | Requisito |
| :----- | :----: | :----: |
| email | **String** | True |
| senha | **String** | True |

<br>

> ### Exemplo de corpo da requisição

```
{
	"email": "usuario@email.com",
	"senha": "****"
}
```

<br>

> ### (200) Exemplo retorno de sucesso

```
{
	"status": 200,
	"message": "OK",
	"data": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkX3VzZXIiOiI5OWJhOWQzZC1jNWFhLTRmMjItYTg3Ni03NGM5OTlkNTU5NjgiLCJleHBpcmVkIjoxNjY4Mjg1NjI2LjkwOTg0Nn0.8KJ3N2G3ay8A05gzfnO_5drSWhbXIuV66HQkYjHDnoM"
}

```

<br>


> ### (401) Exemplo retorno de erro / falha

```
{
	"status": 401,
	"message": "INAUTHORIZED",
	"data": "Usuário não localizado!"
}
```

<br>
<br>
<br>
<br>
<br>
<br>



> ## (POST) /autenticacao/departamento

Essa será a autenticação que será responsável por gerenciar o fluxo de ocorrencias criadas pelos outros usuários. Futuramente será implementado permissões e bloqueios através dos vinculos de tipos de usuários ou diretamente pelo cadastro.

<br>
<br>

### HEADER

* **Content-Type: application/json**

<br>

### BODY
<br>

| Campo | Tipo | Requisito |
| :----- | :----: | :----: |
| email | **String** | True |
| senha | **String** | True |
| departamento | **String** | True |

<br>

> ### Exemplo de corpo da requisição

```
{
	"usuario": "nome_usuario",
	"senha": "*****",
	"departamento": "****"
}
```

<br>

> ### (200) Exemplo retorno de sucesso

```
{
	"status": 200,
	"message": "OK",
	"data": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkX3VzZXIiOiJmZWZlNWUxZS00ZDMwLTRhODktOTZlYS0xNDc0ODVlYTMxZjYiLCJleHBpcmVkIjoxNjY4Mjg3MTkwLjAxNzg3N30.28tGxe20KGhJnbPQUCxOkMtYWDSTh5MWsEeBTYdknkg"
}

```

<br>


> ### (401) Exemplo retorno de erro / falha

```
{
	"status": 401,
	"message": "INAUTHORIZED",
	"data": "Usuário não localizado!"
}
```

<br>
<br>
<br>
<br>
<br>
<br>

### CRUDs

<br>

São as 4 operacçoes básicas utilizadas em conceitos de bando de dados para realizar comandos de leitura, escrita, sobrescrita e exclusão, aqui utilizamos isso como um dos módulos existentes em nossa rotas onde muitas delas serão utilizadas para cadastros simples e necessárias para nosso banco e construção de utilitários.

<br>
<br>
<br>

> ## /usuario/crud

<br>

Rota *CRUD* resposável por cadastrar os novos usuários comuns. Algumas rotas não serão necessárias ser autenticadas, mas nestes casos a informação de autorização não estará presente no cabeçalho.

<br>
<br>
<br>
<br>

> ### (POST) Cadastrar novo usuário comum
<br>

#### HEADER

* **Content-Type: application/json**

<br>
<br>

#### BODY

| Campo | Tipo | Requisito |
| :----- | :----: | :----: |
| nome | **String** | True |
| email | **String** | True |
| cpf | **String** | True |
| senha | **String** | True |
| data_nascimento | **String** | False |

<br>

> ### Exemplo de corpo da requisição

```
{
	"nome": "Fulano",
	"email": "fulano@email.com",
	"cpf": "1111111111111",
	"senha": "1234",
	"data_nascimento": null
}
```

<br>

> ### (200) Exemplo retorno de sucesso

```
{
	"status": 200,
	"message": "OK"
}

```

<br>


> ### (401) Exemplo retorno de erro / falha

```
{
	"status": 401,
	"message": "INAUTHORIZED",
	"data": "Token expirado!"
}
```


<br>
<br>
<br>
<br>


> ### (PUT) Alterar um usuário comum
<br>

#### HEADER

* **Content-Type: application/json**
* **Authorization: Bearer <token>**

<br>
<br>

#### BODY

| Campo | Tipo | Requisito |
| :----- | :----: | :----: |
| nome | **String** | True |
| email | **String** | True |
| cpf | **String** | True |
| senha | **String** | True |
| data_nascimento | **String** | False |

<br>

> ### Exemplo de corpo da requisição

```
{
	"nome": "Fulano",
	"email": "fulano@email.com",
	"cpf": "1111111111111",
	"senha": "1234",
	"data_nascimento": null
}
```

<br>

> ### (200) Exemplo retorno de sucesso

```
{
	"status": 200,
	"message": "OK"
}

```

<br>


> ### (401) Exemplo retorno de erro / falha

```
{
	"status": 401,
	"message": "INAUTHORIZED",
	"data": "Usuário não localizado!"
}
```

<br>
<br>
<br>
<br>


> ### (DELETE) Excluir um usuário comum
<br>

#### HEADER

* **Authorization: Bearer <token>**

<br>
<br>

> ### (200) Exemplo retorno de sucesso

```
{
	"status": 200,
	"message": "OK"
}

```

<br>


> ### (401) Exemplo retorno de erro / falha

```
{
	"status": 401,
	"message": "INAUTHORIZED",
	"data": "Usuário não localizado!"
}
```
