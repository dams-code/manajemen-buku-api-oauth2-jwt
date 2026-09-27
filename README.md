## Manajemen Buku API dengan OAuth2 + JWT

Endpoint Manajemen buku sederhana menggunakan FastAPI dengan JWT (Non-Database)

## Topik sebelum OAuth2 ([link](https://github.com/dams-code/manajemen-buku-api))

- FastAPI
- Path / Query Parameters
- Pydantic BaseModel
- Request Body
- In-Memory Data (Python List)
- Filtering dan CRUD
- HTTPException
- jsonable_encoder
- JSONResponse
- Non-Database

## Topik Oauth Tanpa JWT ([link](https://github.com/dams-code/manajemen-buku-api-oauth2))

 - ✅ APIRouter
 - ✅ Layered Structure
 - ✅ OAuth2 (Non-JWT) (Login User dan Handle CRUD Data Buku)
 - ✅ Registrasi User
 - ✅ Edit Profile User
 - ✅ Ganti Password User
 - ✅ RBAC - Role Based Access
 - ✅ CRUD Buku (Admin saja, manajer hanya sebagai viewer)
 - ✅ CRUD Daftar User (Manajer Saja, jika admin mengeklik - akses ditolak dan di redirect ke 403.html)
 - ✅ Perbaikan Layout dan Membuat (CRUD User - yang dapat melakukan role manajer)

## Topik Oauth + JWT

 - ✅ Mengganti proses create_token, dan verify_token dari itsdangerous menjadi jwt
 - ✅ Perbaikan Kode repositories `user.py` dan `role.py`
 - ✅ Menambahkan BaseModel `TokenData` pada schemas / token

### Perbedaan isi data token.py pada `models/token` dan `schemas/token`

**Pada `models/token`**

```python
@dataclass
class TokenSession():
    access_token: str
    token_type: str
    username: str
```

 > Penggunaan pada repositories/user [result_login](repositories/user.py)

```python
  data_token=TokenSession(
      access_token = access_token,
      token_type="bearer",
      username=form_data.username
  )
```

**Pada `schemas/token`**

```python
class TokenData(BaseModel):
    username: str | None=None
```

| Path | Tipe Class | Keterangan |
| :---: | :---: | :---: |
| schemas/token.py | TokenData(BaseModel) | Untuk parsing payload JWT dari header (client request) dan memvalidasi hasil jika token / payload rusak | 
| models/token.py | TokenSession() | Sebagai internal domain / Entity object pada level app class `tokensession` ini digunakan sepenuhnya didalam aplikasi backend tanpa campur tangan user, dimana hasil data dari tokensession salah satunya dipakai atau dikirim untuk melakukan crosscek sesi aktif user.

### Perbedaan pada itsdangerous vs JWT

<table>
<tr>
<th width="50%">itsdangerous</th>
<th width="50%">PyJWT</th>
</tr>
<tr>
<td valign="top">

```python
GET_SECRET_KEY = os.getenv("SECRET_KEY")

if GET_SECRET_KEY is None:
    raise RuntimeError("File .env belum dibuat / tidak ditemukan")

signer = TimestampSigner(GET_SECRET_KEY)


def create_access_token(username: str):
    token = signer.sign(username).decode("UTF-8")
    return token

def verify_access_token(token: str, umur_token: int = 3600) -> str:
    try:
        username = signer.unsign(token, max_age=umur_token).decode("UTF-8")
        return username
    except SignatureExpired:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token sudah expired / kadaluwarsa",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except BadTimeSignature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

</td>
<td valign="top">

```python
GET_SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITM = "HS256"

if GET_SECRET_KEY is None:
    raise RuntimeError("File .env belum dibuat / tidak ditemukan")
  
def create_access_token(data: dict, expires_delta: timedelta | None=None):
    encode_data = data.copy()

    if expires_delta:
        expires = datetime.now(timezone.utc) + expires_delta
    else:
        expires = datetime.now(timezone.utc) + timedelta(minutes=15)

    encode_data.update({"exp": expires})

    jwt_encode = jwt.encode(encode_data, GET_SECRET_KEY, algorithm=ALGORITM)

    return jwt_encode

def verify_access_token(token: str) -> TokenData:
    cek_kridensial = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Validasi kridensial token gagal",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, GET_SECRET_KEY, algorithms=[ALGORITM])

        username = payload.get('sub')

        if username is None:
            raise cek_kridensial

        token_data = TokenData(username=username)

        return token_data

    except ExpiredSignatureError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Token expired, Login terlebih dahulu",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except InvalidTokenError:
        raise cek_kridensial
```

</td>
</tr>
</table>

#### *Kode diatas dari itsdangerous menjadi PyJWT saya coba ambil dan modifikasi dari situs [fastapi.tiangolo.com](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#update-the-token-path-operation)*

#### Perubahan pada validasi user dan token

<table>
<tr>
<th width="50%">itsdangerous</th>
<th width="50%">PyJWT</th>
</tr>
<tr>
<td valign="top">
  
  ```python
  cek_username_aktif = verify_access_token(token, 3600)

  if cek_username_aktif.lower() != username.lower():
    ...
  ```

</td>
<td>

  ```python
  cek_username_aktif = verify_access_token(token)
  
  if cek_username_aktif.username.lower() != username.lower():
    ...
  ```

</td>
</tr>
</table>

<br/>

## Tech Stack

#### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?style=for-the-badge&logo=uvicorn&logoColor=white)

#### Frontend
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![SweetAlert2](https://img.shields.io/badge/SweetAlert2-8CD4F5?style=for-the-badge&logo=sweetalert2&logoColor=black)

## Copyright Personal Portfolio
* **Project Owner / Created By:** Damar Djati Wahyu Kemala
* **Study:** FastAPI endpoint CRUD buku sederhana versi ke 3 dengan OAuth2 + JWT
* **Date Created:** Agustus 2026
* **GitHub Portfolio:** [https://github.com/dams-code](https://github.com/dams-code)
