from schemas.buku import BukuBase, Buku, ResultBuku
from fastapi import status, HTTPException
from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
from helpers.security import verify_access_token

data_buku = [
    {
        "id": 1,
        "judul": "Laskar Pelangi",
        "penulis": "Andrea hirata",
        "tahun": 2005,
        "genre": "novel",
        "tersedia": True
    },
    {
        "id": 2,
        "judul": "Bumi",
        "penulis": "Tere Liye",
        "tahun": 2014,
        "genre": "fantasty",
        "tersedia": False
    }
]

# async def result_get_buku(id: int | None=None, judul: str | None=None, token: str | None=None) -> ResultBuku[BukuBase | list[BukuBase]]:
async def result_get_buku(id: int | None=None, judul: str | None=None) -> ResultBuku[BukuBase | list[BukuBase]]:
    
    # if token is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Sesi habis, login terlebih dahulu"
    #     )

    # username_aktif = verify_access_token(token, 3600)
    
    if id is not None or judul is not None:
        # result_data_buku = next((item_buku for item_buku in data_buku if (id is not None and item_buku["id"] == id) or (judul is not None and item_buku["judul"].lower() == judul.lower()) ), None)
        result_data_buku = next((item_buku for item_buku in data_buku if (id is not None and item_buku["id"] == id) or (judul is not None and judul.lower() in item_buku["judul"].lower()) ), None)
    
        if result_data_buku is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Buku id {id} tidak ditemukan"
            )
    
        return ResultBuku[BukuBase](
            status= status.HTTP_200_OK,
            pesan= f"Data buku id {result_data_buku["id"]} - judul {result_data_buku["judul"]} berhasil terload",
            data= BukuBase(**result_data_buku)
        )
    
    list_buku = [BukuBase(**item) for item in data_buku]
    
    return ResultBuku[list[BukuBase]](
        status=status.HTTP_200_OK,
        pesan=f"List data buku berhasil terload (total {len(list_buku)} buku)",
        data=list_buku
    )
    
async def result_get_buku_id(id: int) -> ResultBuku[BukuBase]:
    
    # if token is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Sesi habis, login terlebih dahulu",
    #         headers={"WWW-Authenticate": "Bearer"}
    #     )

    # username_aktif = verify_access_token(token, 3600)

    result_data_buku = next((item_buku for item_buku in data_buku if item_buku["id"] == id), None)
    
    if result_data_buku is None:
        return ResultBuku[BukuBase](
            status = status.HTTP_404_NOT_FOUND,
            pesan = f"Buku id {id} tidak ditemukan",
            data = None
        )
    
    return ResultBuku[BukuBase](
        status= status.HTTP_200_OK,
        pesan= f"Data buku id {id} ditemukan",
        data= BukuBase(**result_data_buku)
    )
    
async def result_add_buku(buku: Buku) -> ResultBuku[BukuBase]:
    
    # if token is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Sesi habis, login terlebih dahulu",
    #         headers={"WWW-Authenticate": "Bearer"}
    #     )

    # username_aktif = verify_access_token(token, 3600)

    if not data_buku:
        id_buku = 1
    else:
        list_id = [item_buku.get("id") for item_buku in data_buku]
        id_buku = max(list_id) + 1
        
    result_data_buku = jsonable_encoder(buku)
    
    result_data_buku["id"] = id_buku
    
    data_buku.append(result_data_buku)
    
    return ResultBuku[BukuBase](
        status=status.HTTP_201_CREATED,
        pesan=f"Data buku baru berhasil ditambahkan ke list",
        data= BukuBase(**result_data_buku)
    )
    
async def result_update_buku(id: int, buku: Buku)-> ResultBuku[BukuBase]:
    
    # if token is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Sesi habis, login terlebih dahulu",
    #         headers={"WWW-Authenticate": "Bearer"}
    #     )

    # username_aktif = verify_access_token(token, 3600)

    index_buku = next((index_buku for index_buku, item_buku in enumerate(data_buku) if item_buku["id"] == id), None)
    
    if index_buku is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Buku id {id} tidak ditemukan"
        )
        
    result_update_buku = jsonable_encoder(buku)
    
    result_update_buku["id"] = id
    
    data_buku[index_buku] = result_update_buku
    
    return ResultBuku[BukuBase](
        status=status.HTTP_200_OK,
        pesan=f"Data buku id {id} berhasil diupdate",
        data = BukuBase(**result_update_buku)
    )
    
async def result_delete_buku(id: int) -> ResultBuku[None]:
    
    # if token is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Sesi habis, login terlebih dahulu",
    #         headers={"WWW-Authenticate": "Bearer"}
    #     )

    # username_aktif = verify_access_token(token, 3600)

    index_buku = next((index for index, item_buku in enumerate(data_buku) if item_buku["id"] == id), None)
    
    if index_buku is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data buku id {id} tidak ditemukan"
        )
        
    del data_buku[index_buku]
    
    return ResultBuku[None](
        status=status.HTTP_200_OK,
        pesan=f"Data buku Id {id} berhasil dihapus",
        data=None
    )
    
async def result_update_status_buku(id: int, tersedia: bool) -> ResultBuku[BukuBase]:
    
    # if token is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Sesi habis, login terlebih dahulu",
    #         headers={"WWW-Authenticate": "Bearer"}
    #     )

    # username_aktif = verify_access_token(token, 3600)

    index_buku = next((index for index, item_buku in enumerate(data_buku) if item_buku["id"] == id), None)
    
    if index_buku is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data buku Id {id} tidak ditemukan"
        )
        
    data_buku[index_buku]["tersedia"] = tersedia
    
    return ResultBuku[BukuBase](
        status=status.HTTP_200_OK,
        pesan=f"Status ketersediaan buku Id {id} berhasil diupdate",
        data= BukuBase(**data_buku[index_buku])
    )


