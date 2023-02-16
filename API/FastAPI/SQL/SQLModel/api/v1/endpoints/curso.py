from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.curso_model import CursoModel
from core.deps import get_session


# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True # type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass


router = APIRouter()


# POST Curso
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CursoModel)
async def post_curso(curso: CursoModel, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)

    db.add(novo_curso)
    await db.commit()

    return novo_curso


# GET Cursos
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CursoModel])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()

        return cursos


# GET Curso
@router.get("/{id_curso}", status_code=status.HTTP_200_OK, response_model=CursoModel)
async def get_curso(id_curso: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id_curso)
        result = await session.execute(query)
        curso: CursoModel = result.scalar_one_or_none()

        if curso:
            return curso
        else:
            raise HTTPException(detail="curso não encontrado", status_code=status.HTTP_404_NOT_FOUND)


# PUT Curso
@router.put("/{id_curso}", status_code=status.HTTP_202_ACCEPTED, response_model=CursoModel)
async def put_curso(id_curso: int, curso: CursoModel, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id_curso)
        result = await session.execute(query)
        curso_up: CursoModel = result.scalar_one_or_none()

        if curso_up:
            curso_up.titulo = curso.titulo
            curso_up.aulas = curso.aulas
            curso_up.horas = curso.horas

            await session.commit()

            return curso_up
        else:
            raise HTTPException(detail="curso não encontrado", status_code=status.HTTP_404_NOT_FOUND)


# DELETE Curso
@router.delete("/{id_curso}", status_code=status.HTTP_204_NO_CONTENT)
async def delet_curso(id_curso: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id_curso)
        result = await session.execute(query)
        curso_del: CursoModel = result.scalar_one_or_none()

        if curso_del:
            await session.delete(curso_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="curso não encontrado", status_code=status.HTTP_404_NOT_FOUND)