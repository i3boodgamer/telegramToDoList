import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters import CommandStart, Command

from database.models import User
from utils.states import Form, FormDel
from database.querys import add_item, get_list, del_list

router = Router()


@router.message(CommandStart())
async def start(message: Message, session: AsyncSession) -> None:
    stmt = await session.execute(select(User).where(User.id_user == message.from_user.id))
    result = stmt.scalars().one_or_none()
    print(result)
    if result is None:
        session.add(User(id_user=message.from_user.id))
        await session.commit()
    await message.answer(f"Привет, {message.from_user.first_name}! Я помогу тебе управлять задачами и напоминаниями.")


@router.message(Command("add_task"))
async def start(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await message.answer("Введите описание задачи")
    await state.set_state(Form.description)


@router.message(Form.description)
async def send_photo(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Form.date)
    await message.answer("Введите дату напоминания в формате ГГГГ-ММ-ДД ЧЧ:ММ")


@router.message(Form.date)
async def send_date(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(date=message.text)

    data = await state.get_data()
    await state.clear()

    await add_item(item=data, user_id=message.from_user.id, session=session)


@router.message(Command("all_task"))
async def all_get_task(message: Message, session: AsyncSession):
    lists = await get_list(session=session, user_id=message.from_user.id)
    for item in lists:
        await message.answer(f"Описание: {item.description}.\nВремя напоминания {item.due_date}")


@router.message(Command("del_task"))
async def del_task(message: Message, session: AsyncSession, state: FSMContext):
    await message.answer("Выберите какое напоминание хотите удалить?")

    lists = await get_list(session=session, user_id=message.from_user.id)
    for item in lists:
        await message.answer(f"Номер {item.id}. Описание: {item.description}")

    await state.set_state(FormDel.id_list)


@router.message(FormDel.id_list)
async def del_id_list(message: Message, session: AsyncSession, state: FSMContext):
    await state.update_data(id_list=message.text)

    data = await state.get_data()
    await state.clear()

    await del_list(list_id=int(data["id_list"]), session=session)
    await message.answer(f"Напоминание {data['id_list']} удалено")


