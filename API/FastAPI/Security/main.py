from fastapi import FastAPI

from core.configs import settings
from api.v1.api import api_router


app = FastAPI(title="Curso API - Segurança")
app.include_router(api_router, prefix=settings.API_V1_STR)


"""
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjc5NDAzNTc0LCJpYXQiOjE2Nzg3OTg3NzQsInN1YiI6IjEifQ.OE1F8XvSZTsf6GzZ3cG9_A3u3N5pm9W3A8_ABPX-Xus
Tipo: bearer
"""