from start import app

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




app.http.add_route(AutenticacaoUsuarioController, "/autenticacao/usuario")
app.http.add_route(AutenticaoUsuarioDepartamentoController, "/autenticacao/departamento")
app.http.add_route(CrudUsuariosController, "/usuario/crud", "/usuario/crud/<uuid:user_hash>")
app.http.add_route(CrudUsuariosDepartamentosController, "/departamento/usuario/crud", "/departamento/usuario/crud/<uuid:user_hash>")




