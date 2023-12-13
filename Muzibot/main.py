import asyncio
import logging
import sys
from decouple import config
import time

from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, ParseMode, ReplyKeyboardRemove

from keyboards import Keyboard

from db_module import add, check_user, db_newsfeed, is_player, like_group, like_player,\
    get_player_who_liked, get_group_which_liked, add_to_group_ank, add_to_player_ank, choose_next_func,\
    get_fp_age, all_is_ok, finished_sector, checked_sector, edit_check_point, get_group_data, get_about_player_data,\
    all_is_done, get_check_sector, make_no, clear_genres, get_about_group_data, get_player_data, delete_all,\
    photo_needed, age_needed

TOKEN = config('BOT_TOKEN')

bot = Bot(TOKEN, parse_mode="HTML")

dp = Dispatcher(bot)

check_list = ["group_name", "repetition_base", "about_group", "photo_id", "genres", "gender", "age_range", "add_text",
              "fp_genres", "name", "gender_of_user", "age", "add_text_of_player", "genres", "repetition_base_of_group",
              "fg_genres"]

# group sector


async def give_contact(id_of_chat):
    pass


async def ask_name(id_of_chat: int):
    await bot.send_message(text=f"Как называется твоя группа?",
                           chat_id=id_of_chat)


async def ask_rep_base(id_of_chat: int):
    await bot.send_message(text=f"У вас есть репетиционная база?",
                           chat_id=id_of_chat, reply_markup=Keyboard.true_false_kb())


async def ask_about_group(id_of_chat: int):
    await bot.send_message(text=f"Расскажите о группе",
                           chat_id=id_of_chat, reply_markup=ReplyKeyboardRemove())


async def ask_for_photo(id_of_chat: int):
    await bot.send_message(text=f"Пришли фото его будут видеть другие пользователи",
                           chat_id=id_of_chat)


async def ask_for_genre(id_of_chat: int):
    await bot.send_message(text=f"В каком/-их жанре/-ах вы играете?",
                           chat_id=id_of_chat, reply_markup=await Keyboard.get_genres(id_of_chat))


async def ask_for_player_gender(id_of_chat: int):
    await bot.send_message(text="Замечательно!\n"
                                "Теперь поговорим о том, кого вы ищете\n"
                                "Выберите пол музыканта", chat_id=id_of_chat,
                           reply_markup=await Keyboard.get_gender(id_of_chat))


async def ask_for_player_age(id_of_chat: int):
    if await get_fp_age(id_of_chat) is None:
        await bot.send_message(text="Теперь возраст", chat_id=id_of_chat)
        await bot.send_message(text="От скольки лет вы ищете музыканта?", chat_id=id_of_chat,
                               reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(text="До скольки лет вы ищете музыканта?", chat_id=id_of_chat)


async def ask_add_text(id_of_chat: int):
    await bot.send_message(text="Напишите само объявление. Его будут видеть пользователи", chat_id=id_of_chat,
                           reply_markup=ReplyKeyboardRemove())


async def ask_fp_genres(id_of_chat: int):
    await bot.send_message(text="В каком жанре он должен играть?", chat_id=id_of_chat,
                           reply_markup=await Keyboard.get_genres(id_of_chat))
# player sector


async def ask_player_name(id_of_chat: int):
    await bot.send_message(text=f"Как тебя зовут?", chat_id=id_of_chat)


async def ask_player_gender(id_of_chat: int):
    await bot.send_message(text="Какого ты пола?", chat_id=id_of_chat,
                           reply_markup=await Keyboard.get_gender(id_of_chat))


async def ask_player_age(id_of_chat: int):
    await bot.send_message(text="Сколько тебе лет?", chat_id=id_of_chat, reply_markup=ReplyKeyboardRemove())


async def ask_player_photo(id_of_chat: int):
    await bot.send_message(text=f"Пришли фото его будут видеть другие пользователи",
                           chat_id=id_of_chat)


async def ask_text(id_of_chat: int):
    await bot.send_message(text="Напиши текст о себе. Его будут видеть другие пользователи", chat_id=id_of_chat,
                           reply_markup=ReplyKeyboardRemove())


async def ask_player_genre(id_of_chat: int):
    await bot.send_message(text=f"В каком/-их жанре/-ах вы играете?",
                           chat_id=id_of_chat, reply_markup=await Keyboard.get_genres(id_of_chat))


async def ask_group_rep_base(id_of_chat: int):
    await bot.send_message(text=f"Должна ли быть репетиционная база?",
                           chat_id=id_of_chat, reply_markup=Keyboard.true_false_kb())


async def ask_fg_genres(id_of_chat: int):
    await bot.send_message(text=f"В каком жанре должна играть группа?",
                           chat_id=id_of_chat, reply_markup=await Keyboard.get_genres(id_of_chat))


usr_group = {
    1: lambda x: ask_name(x),
    2: lambda x: ask_rep_base(x),
    3: lambda x: ask_about_group(x),
    4: lambda x: ask_for_photo(x),
    5: lambda x: ask_for_genre(x),
    6: lambda x: echo_group_blank(x),
    7: lambda x: ask_for_player_gender(x),
    8: lambda x: ask_for_player_age(x),
    9: lambda x: ask_add_text(x),
    10: lambda x: ask_fp_genres(x),
    11: lambda x: echo_finding_player_blank(x),
    12: lambda x: user_menu(x)

}

usr_player = {
    1.1: lambda x: ask_player_name(x),
    2.1: lambda x: ask_player_gender(x),
    3.1: lambda x: ask_player_age(x),
    4.1: lambda x: ask_player_photo(x),
    5.1: lambda x: ask_text(x),
    6.1: lambda x: ask_player_genre(x),
    7.1: lambda x: echo_about_player_blank(x),
    8.1: lambda x: ask_group_rep_base(x),
    9.1: lambda x: ask_fg_genres(x),
    10.1: lambda x: echo_finding_group_blank(x),
    11.1: lambda x: user_menu(x)

}


async def acception(id_of_chat):
    await bot.send_message(text="Ваша анкета полностью удалится. Придётся её заполнять заново. Вы согласны?",
                           reply_markup=Keyboard.accept_kb(), chat_id=id_of_chat)


async def execute_func(user_id, func_id):
    if type(func_id) == float:
        await usr_player[func_id](user_id)
    else:
        await usr_group[func_id](user_id)


async def user_menu(id_of_chat: int):
    await bot.send_message(text="Это пользовательское меню, выберите что хотите сделать", chat_id=id_of_chat,
                           reply_markup=Keyboard.user_menu())


async def newsfeed(id_of_chat: int):
    ankets = await db_newsfeed(id_of_chat)
    if await is_player(id_of_chat):
        if ankets == 1:
            await bot.send_message(text="К сожалению, нет подходящих тебе объявлений",
                                   chat_id=id_of_chat, reply_markup=Keyboard.back_to_menu())

        else:
            await bot.send_photo(chat_id=id_of_chat, photo=ankets[0]["photo_id"],
                                 caption=f"Название группы: {ankets[0]['group_name']}\n"
                                         f"Наличие репетиционной базы: {ankets[0]['repetition_base']}\n"
                                         f"Объявление: {ankets[0]['about_group']}\n",
                                 reply_markup=Keyboard.like_dislike(ankets[0]["user_id"]))
    else:
        if ankets == 1:
            await bot.send_message(text="К сожалению, нет подходящих тебе объявлений",
                                   chat_id=id_of_chat, reply_markup=Keyboard.back_to_menu())
        else:
            await bot.send_message(chat_id=id_of_chat, text=f"Имя: {ankets[0]['name']}\n"
                                                            f"возраст: {ankets[0]['age']}\n"
                                                            f"Пол: {ankets['gender_of_user']}\n"
                                                            f"Объявление: {ankets[0]['add_text_of_player']}\n",
                                   reply_markup=Keyboard.like_dislike(ankets[0]["user_id"]))


async def notify(id_of_chat):
    if await is_player(id_of_chat):
        ankets = await get_group_which_liked(id_of_chat)
        if ankets == 1:
            await bot.send_message(text="Нет уведомлений",
                                   chat_id=id_of_chat, reply_markup=Keyboard.back_to_menu())
        else:
            await bot.send_photo(chat_id=id_of_chat, photo=ankets[0]["photo_id"],
                                 caption=f"Название группы: {ankets[0]['group_name']}\n"
                                         f"Наличие репетиционной базы: {ankets[0]['repetition_base']}\n"
                                         f"Объявление: {ankets[0]['about_group']}\n",
                                 reply_markup=Keyboard.answer_kb())
    else:
        ankets = await get_player_who_liked(id_of_chat)
        if ankets == 1:
            await bot.send_message(text="Нет уведомлений",
                                   chat_id=id_of_chat, reply_markup=Keyboard.back_to_menu())
        else:
            await bot.send_message(chat_id=id_of_chat,
                                   text=f"Имя: {ankets[0]['name']}\n"
                                        f"возраст: {ankets[0]['age']}\n"
                                        f"Пол: {ankets[0]['gender_of_user']}\n"
                                        f"Объявление: {ankets[0]['add_text_of_player']}\n",
                                   reply_markup=Keyboard.answer_kb())


async def edit_form(id_of_chat: int, sector: str):
    if sector == "check_g_part":
        await bot.send_message(text="Что вы хотите изменить?", reply_markup=Keyboard.edit_group_form_kb(),
                               chat_id=id_of_chat)
    elif sector == "check_fp_part":
        await bot.send_message(text="Что вы хотите изменить?", chat_id=id_of_chat,
                               reply_markup=Keyboard.edit_finding_player_form_kb())
    elif sector == "check_g_part":
        await bot.send_message(text="Что вы хотите изменить?", chat_id=id_of_chat,
                               reply_markup=Keyboard.edit_finding_group_form_kb())
    elif sector == "check_p_part":
        await bot.send_message(text="Что вы хотите изменить?", chat_id=id_of_chat,
                               reply_markup=Keyboard.edit_about_player_form())


async def echo_group_blank(id_of_chat: int):
    data = await get_group_data(id_of_chat)
    await bot.send_message(chat_id=id_of_chat, text="Убедитесь, что ваша анкета заполнена правильно!",
                           reply_markup=ReplyKeyboardRemove())
    await bot.send_photo(chat_id=id_of_chat, photo=data[0]["photo_id"],
                         caption=f"Название группы: {data[0]['group_name']}\n"
                                 f"Жанр: {', '.join([i[0]['name'] for i in [j for j in data[1:]]])}\n"
                                 f"Наличие репетиционной базы: {data[0]['repetition_base']}\n"
                                 f"О группе: {data[0]['about_group']}\n\n"
                                 f"Всё правильно?", reply_markup=Keyboard.true_edit_kb())


async def echo_finding_player_blank(id_of_chat):
    data = await get_about_player_data(id_of_chat)
    await bot.send_message(chat_id=id_of_chat, text="Убедитесь, что check list искомого музыканта заполнен правильно!",
                           reply_markup=ReplyKeyboardRemove())
    await bot.send_message(chat_id=id_of_chat,
                           text=f"Кого ищешь: \n"
                                f"Пол: {data[0]['gender']}\n"
                                f"Возраст от {str(data[0]['age_range'])[0:2]} "
                                f"до {str(data[0]['age_range'])[2:]}\n"
                                f"Жанр: {', '.join([i[0]['name'] for i in [j for j in data[1:]]])}\n"
                                f"Текст объявления:\n {data[0]['add_text']}\n\n"
                                f"Всё правильно?", reply_markup=Keyboard.true_edit_kb())


async def echo_finding_group_blank(id_of_chat):
    data = await get_about_group_data(id_of_chat)
    await bot.send_message(chat_id=id_of_chat, text="Убедитесь, что check list искомой группы заполнен правильно!",
                           reply_markup=ReplyKeyboardRemove())
    await bot.send_message(chat_id=id_of_chat, text=f"Кого ищешь: Группу\n"
                                                    f"Жанр: {', '.join([i[0]['name'] for i in [j for j in data[1:]]])}\n"
                                                    f"Наличие репетиционной базы: "
                                                    f"{data[0]['repetition_base_of_group']}\n\n"
                                                    f"Всё правильно?", reply_markup=Keyboard.true_edit_kb())


async def echo_about_player_blank(id_of_chat):
    data = await get_player_data(id_of_chat)
    await bot.send_message(chat_id=id_of_chat, text="Убедитесь, что ваша анкета заполнена правильно!",
                           reply_markup=ReplyKeyboardRemove())
    await bot.send_photo(chat_id=id_of_chat, photo=data[0]["photo_id"],
                         caption=f"О себе: \n"
                                 f"Имя: {data[0]['name']}\n"
                                 f"Пол: {data[0]['gender_of_user']}\n"
                                 f"Возраст: {data[0]['age']}\n"
                                 f"Твой жанр: {', '.join([i[0]['name'] for i in [j for j in data[1:]]])}\n"
                                 f"О себе:\n {(data[0]['add_text_of_player'])}\n\n"
                                 f"Всё правильно?", reply_markup=Keyboard.true_edit_kb())


@dp.message_handler(commands=['start'])
async def bot_start(message: Message):
    if await check_user(message.from_user.id):
        await user_menu(message.from_user.id)
    else:
        await message.answer("Кого ты ищешь?", reply_markup=Keyboard.start_keyboard())


@dp.callback_query_handler()
async def start_callback(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if callback_query.data == "notify":
        await notify(callback_query.from_user.id)
    elif callback_query.data == "newsfeed":
        await newsfeed(callback_query.from_user.id)
    elif callback_query.data == "user_menu":
        await user_menu(callback_query.from_user.id)
    elif callback_query.data == "dislike":
        await newsfeed(callback_query.from_user.id)
    elif callback_query.data == "ignore":
        await notify(callback_query.from_user.id)
    elif callback_query.data.split("/")[0] == "like":
        if await is_player(callback_query.from_user.id):
            await like_group(callback_query.from_user.id, callback_query.data.split("/")[1])
            await newsfeed(callback_query.from_user.id)
        else:
            await like_player(callback_query.from_user.id, callback_query.data.split("/")[1])
            await newsfeed(callback_query.from_user.id)
    elif callback_query.data == "write":
        await bot.send_message(text=f"<a href='tg://user?id=751217450'>Нажми,чтобы написать</a>",
                               chat_id=callback_query.from_user.id,
                               parse_mode=ParseMode.HTML)
    elif callback_query.data == "change":
        await delete_all(callback_query.from_user.id)
        await bot.send_message(chat_id=callback_query.from_user.id, text="Кого ты ищешь?",
                               reply_markup=Keyboard.start_keyboard())
    elif callback_query.data == "no_change":
        await user_menu(callback_query.from_user.id)
    elif callback_query.data == "group":
        await add_to_player_ank(callback_query.from_user.id)
        await usr_player[1.1](callback_query.from_user.id)
    elif callback_query.data == "musician":
        await add_to_group_ank(callback_query.from_user.id)
        await usr_group[1](callback_query.from_user.id)
    elif callback_query.data == "back":
        next_func = await choose_next_func(callback_query.from_user.id)
        await execute_func(callback_query.from_user.id, next_func)
    elif callback_query.data == "change_ank":
        await acception(callback_query.from_user.id)
    elif callback_query.data == "Да":
        if await finished_sector(callback_query.from_user.id):
            statement = await finished_sector(callback_query.from_user.id)
            if statement[0]:
                await add(callback_query.from_user.id, callback_query.data)
                next_func = await choose_next_func(callback_query.from_user.id)
                await execute_func(callback_query.from_user.id, next_func)
        elif await all_is_done(callback_query.from_user.id):
            await newsfeed(callback_query.from_user.id)
        else:
            if await checked_sector(callback_query.from_user.id)[0]:
                sector = await checked_sector(callback_query.from_user.id)[1]
                await edit_check_point(callback_query.from_user.id, sector)
                if await all_is_ok(callback_query.from_user.id):
                    await newsfeed(callback_query.from_user.id)
                else:
                    next_func = await choose_next_func(callback_query.from_user.id)
                    await execute_func(callback_query.from_user.id, next_func)
    elif callback_query.data == "Нет":
        if await finished_sector(callback_query.from_user.id):
            statement = await finished_sector(callback_query.from_user.id)
            if statement[0]:
                await add(callback_query.from_user.id, callback_query.data)
                next_func = await choose_next_func(callback_query.from_user.id)
                await execute_func(callback_query.from_user.id, next_func)
        else:
            if await checked_sector(callback_query.from_user.id)[0]:
                sector = await checked_sector(callback_query.from_user.id)[1]
                await edit_form(callback_query.from_user.id, sector)
    elif callback_query.data in check_list:
        if callback_query.data in ["genres", "fp_genres", "fg_genres"]:
            await clear_genres(callback_query.from_user.id)
            await make_no(callback_query.from_user.id, callback_query.data)
            next_func = await choose_next_func(callback_query.from_user.id)
            await execute_func(callback_query.from_user.id, next_func)
        else:
            await make_no(callback_query.from_user.id, callback_query.data)
            next_func = await choose_next_func(callback_query.from_user.id)
            await execute_func(callback_query.from_user.id, next_func)
    elif callback_query.data == "Изменить":
        sector = await get_check_sector(callback_query.from_user.id)
        await edit_form(callback_query.from_user.id, sector)
    else:
        await add(callback_query.from_user.id, callback_query.data)
        next_func = await choose_next_func(callback_query.from_user.id)
        await execute_func(callback_query.from_user.id, next_func)


@dp.message_handler(content_types=['document', 'photo', 'text'])
async def handler(message: Message):
    if photo_needed(message.from_user.id):
        if message.content_type == "photo":
            photos = message.photo
            new_id = photos[-1].file_id
            await add(message.from_user.id, new_id)
            next_func = await choose_next_func(message.from_user.id)
            await execute_func(message.from_user.id, next_func)
        else:
            await message.answer(text="Нам нужна картинка!")
    elif age_needed(message.from_user.id):
        try:
            age = int(message.text)
        except ValueError:
            await message.answer(text="Введите число!")
        else:
            await add(message.from_user.id, int(message.text))
            next_func = await choose_next_func(message.from_user.id)
            await execute_func(message.from_user.id, next_func)
    else:
        await add(message.from_user.id, message.text)
        next_func = await choose_next_func(message.from_user.id)
        await execute_func(message.from_user.id, next_func)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
