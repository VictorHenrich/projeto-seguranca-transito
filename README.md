# Documentação API - Segurança no trânsito

<br>
<br>

## Descrição

Este é meu projeto de TCC: um sistema web com foco em auxiliar as pessoas em casos de acidentes de trânsito. O objetivo principal é fornecer informações sobre os protocolos corretos a serem seguidos, além de facilitar o registro de boletins de ocorrência para possíveis ações jurídicas no futuro. O sistema será acessado por meio de um aplicativo para dispositivos móveis, considerado hoje um dos itens essenciais para a maioria das pessoas. Essa abordagem permitirá que tudo seja feito de forma prática e conveniente, utilizando apenas o celular, como é comum nos dias de hoje.

A documentação aqui apresentada abrange as funcionalidades oferecidas por meio de rotas via API. Essas rotas possibilitarão a realização da maior parte do gerenciamento realizado pelo aplicativo, desde a autenticação até o controle das ocorrências já criadas ou que ainda serão criadas.

<br>
<br>
<br>

## Autenticação

A autenticação do usuário é realizada por meio do seu e-mail e senha previamente cadastrados. Caso você ainda não tenha uma conta, utilize a rota de cadastro de usuário para prosseguir.

<br>
<br>

> ## (POST) /usuario/autenticacao
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

## Cadastro de usuário

Esta rota tem a responsabilidade de cadastrar um usuário e gerar sua conta de acesso. Para isso, serão necessárias algumas informações pessoais do usuário. Além disso, é obrigatório cadastrar pelo menos um veículo.

<br>
<br>

> ## (POST) /usuario/registro

<br>
<br>

### HEADER

* **Content-Type: application/json**

<br>

### BODY USER
<br>

| Campo | Tipo | Requisito |
| :----- | :----: | :----: |
| email | **String** | True |
| senha | **String** | True |
| cpf | **String** | True |
| rg | **String** | True |
| estado_emissor | **String** | True |
| telefone | **String** | True |
| data_nascimento | **DateString** | True |
| endereco_uf | **String** | True |
| endereco_cidade | **String** | True |
| endereco_bairro | **String** | True |
| endereco_logradouro | **String** | True |
| endereco_numero | **String** | True |
| veiculos | **Array<Vehicle>** | True |


### BODY VEHICLE
<br>

| Campo | Tipo | Requisito |
| :----- | :----: | :----: |
| placa | **String** | True |
| renavam | **String** | True |
| tipo_veiculo | **LiteralString<"CARRO", "MOTO">** | True |
| marca | **String** | False |
| chassi | **String** | False |
| cor | **String** | False |
| ano | **String | Number** | False |
| possui_seguro | **Boolean** | False |


<br>

> ### Exemplo de corpo da requisição

```
{
	"email": "usuario@email.com",
	"senha": "****",
	"cpf": "XXX.XXX.XXX-XX",
	"rg": "YYYYYYYYYY",
	"telefone": "48999999999",
	"data_nascimento": "1998-05-27",
	"estado_emissor": "SANTA CATARINA",
	"endereco_uf": "SC",
	"endereco_cidade": "Tubarão",
	"endereco_bairro": "Andrino",
	"endereco_logradouro": "Minha rua é",
	"endereco_numero": "S/N",
	"veiculos": [
		{
			"placa": "XXXXXX-XXXX",
			"renavam": "IIIIIIIII",
			"tipo_veiculo": "CARRO"
		},
		{
			"placa": "ZZZZZZZ-XXXX",
			"renavam": "UUUUUUUU",
			"tipo_veiculo": "MOTO"
		}
	]
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
