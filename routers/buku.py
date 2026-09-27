from schemas.roles import Roles
from fastapi import APIRouter, Query, Path, Depends
from repositories.buku import *
from schemas.buku import ResultBuku, Buku
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from repositories.roles import CekRole

router_buku = APIRouter(prefix="/buku", tags=["buku"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router_buku.get("", response_model=ResultBuku[BukuBase | list[BukuBase]], dependencies=[Depends(CekRole([Roles.ADMIN, Roles.MANAJER]))])
# async def get_buku(id: Annotated[int | None, Query()] = None, judul: Annotated[str | None, Query()] = None, token: Annotated[str, Depends(oauth2_scheme)] = None):
async def get_buku(id: Annotated[int | None, Query()] = None, judul: Annotated[str | None, Query()] = None):
    
    return await result_get_buku(id=id, judul=judul)


@router_buku.get("/{id}", response_model=ResultBuku[BukuBase], dependencies=[Depends(CekRole([Roles.ADMIN, Roles.MANAJER]))])
# async def get_buku_id(id: Annotated[int, Path(description="Cari Id Buku", gt=0)], token: Annotated[str, Depends(oauth2_scheme)] = None):
async def get_buku_id(id: Annotated[int, Path(description="Cari Id Buku", gt=0)]):
    
    return await result_get_buku_id(id=id)

@router_buku.post("", response_model=ResultBuku[BukuBase], status_code=status.HTTP_201_CREATED, dependencies=[Depends(CekRole([Roles.ADMIN]))])
# async def add_buku(buku: Buku, token: Annotated[str, Depends(oauth2_scheme)] = None):
async def add_buku(buku: Buku):
    
    return await result_add_buku(buku)

@router_buku.put("/{id}", response_model=ResultBuku[BukuBase], dependencies=[Depends(CekRole([Roles.ADMIN]))])
# async def update_buku(id: Annotated[int, Path(description="Update Id Buku", gt=0)], buku: Buku, token: Annotated[str, Depends(oauth2_scheme)] = None):
async def update_buku(id: Annotated[int, Path(description="Update Id Buku", gt=0)], buku: Buku):
    
    return await result_update_buku(id=id, buku=buku)

@router_buku.delete("/{id}", response_model=ResultBuku[None], dependencies=[Depends(CekRole([Roles.ADMIN]))])
async def delete_buku(id: Annotated[int, Path(description="Hapus Id Buku", gt=0)]):
# async def delete_buku(id: Annotated[int, Path(description="Hapus Id Buku", gt=0)], token: Annotated[str, Depends(oauth2_scheme)] = None):
    
    return await result_delete_buku(id=id)

@router_buku.patch("/{id}", response_model=ResultBuku[BukuBase], dependencies=[Depends(CekRole([Roles.ADMIN]))])
# async def update_status_buku(id: Annotated[int, Path(description="Update Status Buku", gt=0)], tersedia: Annotated[bool, Query(description="Ketersedian buku (true/false)")], token: Annotated[str, Depends(oauth2_scheme)] = None):
async def update_status_buku(id: Annotated[int, Path(description="Update Status Buku", gt=0)], tersedia: Annotated[bool, Query(description="Ketersedian buku (true/false)")]):
    
    return await result_update_status_buku(id=id, tersedia=tersedia)
