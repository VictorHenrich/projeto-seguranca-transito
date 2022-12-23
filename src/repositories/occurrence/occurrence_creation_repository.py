from dataclasses import dataclass

from patterns.repository import BaseRepository
from models import Ocorrencia, Usuario, Departamento



@dataclass
class OccurrenceCreationRepositoryParam:
    user: Usuario
    departament: Departamento
    description: str
    obs: str



class OccurrenceCreationRepository(BaseRepository):
    def create(self, param: OccurrenceCreationRepositoryParam) -> None:
        occurrence: Ocorrencia = Ocorrencia()

        occurrence.id_departamento = param.departament.id
        occurrence.id_usuario = param.user.id
        occurrence.descricao = param.description
        occurrence.obs = param.obs
        occurrence.status = "ANDAMENTO"

        self.session.add(occurrence)