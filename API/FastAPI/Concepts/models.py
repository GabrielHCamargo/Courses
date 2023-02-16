from typing import Optional

from pydantic import BaseModel, validator


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int


    @validator("titulo")
    def validar_titulo(cls, value: str):
        palavras = value.split(" ")
        if len(palavras) < 3:
            raise ValueError("o titulo deve ter no mínimo 3 palavras")
        
        if value.islower():
            raise ValueError("o titulo deve ser capitalizado")

        return value

    
    @validator("aulas")
    def validar_aulas(cls, value: int):
        if value <= 12:
            raise ValueError("as aulas devem ser maiores que 12")

        return value


    @validator("horas")
    def validar_horas(cls, value: int):
        if value <= 10:
            raise ValueError("as horas devem ser maiores que 10")

        return value


cursos = [
    Curso(id=1, titulo="Curso de Python", aulas=50, horas=100),
    Curso(id=2, titulo="Curso de Java", aulas=30, horas=300),
]