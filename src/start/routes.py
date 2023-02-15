from start import app

from controllers.http.autenticacao import (
    AutenticacaoUsuarioController,
    AutenticaoUsuarioDepartamentoController,
)
from controllers.http.usuarios import CrudUsuariosController
from controllers.http.usuarios_departamento import CrudUsuariosDepartamentosController
from controllers.http.ocorrencias import CrudOcorrenciasController


# AUTENTICAÇÃO
app.http.add_route(AutenticacaoUsuarioController, "/autenticacao/usuario")
app.http.add_route(
    AutenticaoUsuarioDepartamentoController, "/autenticacao/departamento"
)

# CRUD DE CLIENTES
app.http.add_route(
    CrudUsuariosController, "/usuario/crud", "/usuario/crud/<uuid:user_hash>"
)

# CRUD DE USUÁRIOS DE DEPARTAMENTO
app.http.add_route(
    CrudUsuariosDepartamentosController,
    "/departamento/usuario/crud",
    "/departamento/usuario/crud/<uuid:user_hash>",
)

# CRUD DE OCORRÊNCIAS
app.http.add_route(
    CrudOcorrenciasController,
    "/ocorrencia/crud",
    "/ocorrencia/crud/<uuid:occurrence_hash>",
)
