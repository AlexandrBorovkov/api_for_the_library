from fastapi import APIRouter, Depends

from src.librarians.dependencies import get_current_user
from src.librarians.models import Librarian
from src.readers.dao import ReaderDAO
from src.readers.schemas import SReader

router = APIRouter(prefix="/readers", tags=["Readers"])

@router.get("/reader")
async def show_reader(
    reader_id: int,
    librarian: Librarian = Depends(get_current_user)
):
    result = await ReaderDAO.find_by_id(reader_id)
    return result

@router.get("/all_readers")
async def get_readers(librarian: Librarian = Depends(get_current_user)):
    result = await ReaderDAO.get_readers()
    return result

@router.post("/add_reader")
async def add_reader(
    reader: SReader,
    librarian: Librarian = Depends(get_current_user)
):
    await ReaderDAO.add_reader(
        name=reader.name,
        email=reader.email
    )

@router.delete("/delete_reader")
async def delete_reader(
    reader_id: int,
    librarian: Librarian = Depends(get_current_user)
):
    await ReaderDAO.delete_reader(reader_id)

@router.patch("/update_reader")
async def update_reader(
    reader_id: int,
    reader: SReader,
    librarian: Librarian = Depends(get_current_user)
):
    await ReaderDAO.update_reader(
        reader_id,
        name=reader.name,
        email=reader.email
    )
