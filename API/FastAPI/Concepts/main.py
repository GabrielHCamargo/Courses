from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi import Response

from models import Curso


app = FastAPI()


cursos = {
    1: {
        "titulo": "Titulo do Curso",
        "aulas": 112,
        "horas": 58,
    },
    2: {
        "titulo": "Titulo do Curso 2",
        "aulas": 112,
        "horas": 58,
    },
}


@app.get("/cursos")
async def get_cursos():
    return cursos


@app.get("/cursos/{curso_id}")
async def get_curso(curso_id: int):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="curso não encontrado"
        )


@app.post("/cursos", status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso):
    next_id: int = len(cursos) + 1
    del curso.id
    cursos[next_id] = curso
    return curso


@app.put("/cursos/{curso_id}")
async def put_curso(curso_id: int, curso: Curso):
    if curso_id in cursos:
        del curso.id
        cursos[curso_id] = curso
        return curso
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"curso com o id: {curso_id}, não foi encontrado",
        )


@app.delete("/cursos/{curso_id}")
async def delete_curso(curso_id: int):
    if curso_id in cursos:
        del cursos[curso_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"curso com o id: {curso_id}, não foi encontrado",
        )
