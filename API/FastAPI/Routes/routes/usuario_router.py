from fastapi import APIRouter


router = APIRouter()


@router.get("/api/v1/usuarios")
async def get_router():
    return {"info": "todos os usuários"}