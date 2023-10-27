from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from functionals.logging import files

#
document_router = Router()


class Documents(StatesGroup):
    text = State()


@document_router.message(Documents.text)
async def add_document(message: types.Message, state: FSMContext):
    document = message.document
    file_id = document.file_id
    file_name = document.file_name
    await files.add_file(file_id, file_name)
    await state.clear()
    await message.answer(f"Добавили файл {file_name}.")

