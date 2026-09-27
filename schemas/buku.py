from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class BukuBase(BaseModel):
    id: int
    judul: str
    penulis: str
    tahun: int
    genre: str
    tersedia: bool

class Buku(BaseModel):
    judul: str
    penulis: str
    tahun: int
    genre: str
    tersedia: bool
    
class ResultBuku(BaseModel, Generic[T]):
    status: int
    pesan: str
    data: Optional[T] = None