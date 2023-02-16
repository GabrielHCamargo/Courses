from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
from fastapi import Path
from fastapi import Query
from fastapi import Header
from fastapi import Depends

from typing import Optional, Any, List, Dict

from time import sleep

from models import Curso
from models import cursos


app = FastAPI(
    title="API para Estudo",
    description="API para Estudando usando o FastAPI",
    version="0.0.1",
)


async def fake_db():
    try:
        print("Inicianco conexão com Banco de Dados...")
        sleep(1)
    finally:
        print("Encerrando conexão com Banco de Dados...")
        sleep(1)


@app.get(
    "/cursos",
    summary="Retornar todos os cursos",
    description="Retorna todos os curso ou uma lista vazia",
    response_description="Cursos encontrados com sucesso"
)
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos


@app.get(
    "/cursos/{curso_id}",
    summary="Retornar um curso",
    description="Retornar um curso específico pelo ID se encontrado",
    response_description="Curso encontrado com sucesso",
)
async def get_curso(curso_id: int = Path(default=None, gt=0, lt=4, title="ID do Curso", description="Valores menores que 3"), db: Any = Depends(fake_db)):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="curso não encontrado"
        )


@app.post(
    "/cursos",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar novo curso",
    description="Cadastrar um curso novo",
    response_description="Curso cadastrado com sucesso",
)
async def post_curso(curso: Curso, db: Any = Depends(fake_db)):
    next_id: int = len(cursos) + 1
    curso.id = next_id
    cursos.append(curso)
    return curso


@app.put(
    "/cursos/{curso_id}",
    summary="Atualizar um curso",
    description="Atualizar um curso existente",
    response_description="Curso atualizado com sucesso",
)
async def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        del curso.id
        cursos[curso_id] = curso
        return curso
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"curso com o id: {curso_id}, não foi encontrado",
        )


@app.delete(
    "/cursos/{curso_id}", summary="Apagar um curso",
    description="Apagar um curso existente",
    response_description="Curso apagado com sucesso",
)
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        del cursos[curso_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"curso com o id: {curso_id}, não foi encontrado",
        )


@app.get(
    "/calcular",
    summary="Calcular",
    description="Somar 2 ou 3 números",
    response_model=Dict[str, int],
    response_description="Número com sucesso",
)
async def calcular(x_geek: str = Header(default=None), a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), c: Optional[int] = None):
    soma = a + b
    if c:
        soma = soma + c
    print(f"X-GEEK: {x_geek}")
    return {"resultado": soma}
