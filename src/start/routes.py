from start import server

from controllers.http.autenticacao import (
    AutenticacaoUsuarioController, 
    AutenticaoUsuarioDepartamentoController
)
from controllers.http.usuarios import (
    CrudUsuariosController
)
from controllers.http.usuarios_departamento import (
    CrudUsuariosDepartamentosController
)




server.http.add_route(AutenticacaoUsuarioController, "/autenticacao/usuario")
server.http.add_route(AutenticaoUsuarioDepartamentoController, "/autenticacao/departamento")
server.http.add_route(CrudUsuariosController, "/usuario/crud", "/usuario/crud/<uuid:user_hash>")
server.http.add_route(CrudUsuariosDepartamentosController, "/departamento/usuario/crud", "/departamento/usuario/crud/<uuid:user_hash>")




