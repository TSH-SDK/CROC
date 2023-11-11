import asyncio
import logging
import sys
from decouple import config
import time

from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, ParseMode, ReplyKeyboardRemove

from keyboards import Keyboard
from data import add_info_for_bot, about_player_info_form, about_group_info_form, finding_player_info_form,\
    finding_group_info_form
from db_module import add_player, add_group, check_user, db_newsfeed, is_player, like_group, like_player,\
    get_player_who_liked, get_group_which_liked

TOKEN = config('BOT_TOKEN')

bot = Bot(TOKEN, parse_mode="HTML")

dp = Dispatcher(bot)


async def user_menu(id_of_chat: int):
    await bot.send_message(text="Это пользовательское меню, выберите что хотите сделать", chat_id=id_of_chat,
                           reply_markup=Keyboard.user_menu())


async def newsfeed(id_of_chat: int):
    ankets = await db_newsfeed(id_of_chat)
    add_info_for_bot["last_id"] = ankets[add_info_for_bot["n"]][0]["user_id"]
    if await is_player(id_of_chat):
        if len(ankets) == 0 or ankets[add_info_for_bot["n"]][0]["photo_id"] == ankets[-1][0]["photo_id"]:
            if len(ankets) == 0:
                await bot.send_message(text="К сожалению, нет подходящих тебе объявлений",
                                       chat_id=id_of_chat, reply_markup=Keyboard.back_to_menu())

            else:
                add_info_for_bot["last"] = True
                await bot.send_photo(chat_id=id_of_chat, photo=ankets[add_info_for_bot['n']][0]["photo_id"],
                                     caption=f"Название группы: {ankets[add_info_for_bot['n']][0]['group_name']}\n"
                                             f"Наличие репетиционной базы: {ankets[add_info_for_bot['n']][0]['repetition_base']}\n"
                                             f"Объявление: {ankets[add_info_for_bot['n']][0]['about_group']}\n",
                                     reply_markup=Keyboard.like_dislike())
                add_info_for_bot["n"] = 0

                await bot.send_message(text="К сожалению, это последнее подходящее тебе объявление",
                                       chat_id=id_of_chat, reply_markup=Keyboard.back_to_menu())
        else:
            add_info_for_bot["n"] += 1
            await bot.send_photo(chat_id=id_of_chat, photo=ankets[add_info_for_bot['n']][0]["photo_id"],
                                caption=f"Название группы: {ankets[add_info_for_bot['n']][0]['group_name']}\n"
                                     f"Наличие репетиционной базы: {ankets[add_info_for_bot['n']][0]['repetition_base']}\n"
                                     f"Объявление: {ankets[add_info_for_bot['n']][0]['about_group']}\n",
                                 reply_markup=Keyboard.like_dislike())
    else:
        if len(ankets) == 0 or ankets[add_info_for_bot["n"]][0]["players_id"] == ankets[-1][0]["players_id"]:
            if len(ankets) == 0:
                await bot.send_message(text="К сожалению, нет подходящих тебе объявлений",
                                       chat_id=id_of_chat, reply_markup=Keyboard.back_to_menu())

            else:
                await bot.send_message(chat_id=id_of_chat, text=f"Имя: {ankets[add_info_for_bot['n']][0]['name']}\n"
                                f"возраст: {ankets[add_info_for_bot['n']][0]['age']}\n"
                                f"Пол: {ankets[add_info_for_bot['n']][0]['gender_of_user']}\n"
                                f"Объявление: {ankets[add_info_for_bot['n']][0]['add_text_of_player']}\n",
                                reply_markup=Keyboard.like_dislike())
                add_info_for_bot["n"] = 0
                add_info_for_bot["last"] = True
                await bot.send_message(text="К сожалению, это последнее подходящее тебе объявление",
                                       chat_id=id_of_chat, reply_markup=Keyboard.back_to_menu())
        else:
            add_info_for_bot["n"] += 1
            await bot.send_message(chat_id=id_of_chat, text=f"Имя: {ankets[add_info_for_bot['n']][0]['name']}\n"
                                                            f"возраст: {ankets[add_info_for_bot['n']][0]['age']}\n"
                                                            f"Пол: {ankets[add_info_for_bot['n']][0]['gender_of_user']}\n"
                                                            f"Объявление: {ankets[add_info_for_bot['n']][0]['add_text_of_player']}\n",
                                   reply_markup=Keyboard.like_dislike())


async def notify(id_of_chat):
    if await is_player(id_of_chat):
        ankets = await get_group_which_liked(id_of_chat)
        if len(ankets) == 0 or ankets[add_info_for_bot["n"]][0]["photo_id"] == ankets[-1][0]["photo_id"]:
            if len(ankets) == 0:
                await bot.send_message(text="Нет уведомлений",
                                       chat_id=id_of_chat, reply_markup=Keyboard.back_to_menu())

            else:
                add_info_for_bot["last"] = True
                await bot.send_photo(chat_id=id_of_chat, photo=ankets[add_info_for_bot['n']][0]["photo_id"],
                                     caption=f"Название группы: {ankets[add_info_for_bot['n']][0]['group_name']}\n"
                                             f"Наличие репетиционной базы: {ankets[add_info_for_bot['n']][0]['repetition_base']}\n"
                                             f"Объявление: {ankets[add_info_for_bot['n']][0]['about_group']}\n",
                                     reply_markup=Keyboard.answer_kb())
                add_info_for_bot["n"] = 0
                await bot.send_message(text="Это последнее уведомление",
                                       chat_id=id_of_chat, reply_markup=Keyboard.back_to_menu())
        else:
            add_info_for_bot["n"] += 1
            await bot.send_photo(chat_id=id_of_chat, photo=ankets[add_info_for_bot['n']][0]["photo_id"],
                                 caption=f"Название группы: {ankets[add_info_for_bot['n']][0]['group_name']}\n"
                                         f"Наличие репетиционной базы: {ankets[add_info_for_bot['n']][0]['repetition_base']}\n"
                                         f"Объявление: {ankets[add_info_for_bot['n']][0]['about_group']}\n",
                                 reply_markup=Keyboard.answer_kb())
    else:
        ankets = await get_player_who_liked(id_of_chat)
        if len(ankets) == 0 or ankets[add_info_for_bot["n"]][0]["players_id"] == ankets[-1][0]["players_id"]:
            if len(ankets) == 0:
                await bot.send_message(text="Нет уведомлений",
                                       chat_id=id_of_chat, reply_markup=Keyboard.back_to_menu())

            else:
                add_info_for_bot["last"] = True
                await bot.send_message(chat_id=id_of_chat, text=f"Имя: {ankets[add_info_for_bot['n']][0]['name']}\n"
                                                                f"возраст: {ankets[add_info_for_bot['n']][0]['age']}\n"
                                                                f"Пол: {ankets[add_info_for_bot['n']][0]['gender_of_user']}\n"
                                                                f"Объявление: {ankets[add_info_for_bot['n']][0]['add_text_of_player']}\n",
                                       reply_markup=Keyboard.answer_kb())
                add_info_for_bot["n"] = 0

                await bot.send_message(text="К сожалению, это последнее подходящее тебе объявление",
                                       chat_id=id_of_chat, reply_markup=Keyboard.back_to_menu())
        else:
            add_info_for_bot["n"] += 1
            await bot.send_message(chat_id=id_of_chat, text=f"Имя: {ankets[add_info_for_bot['n']][0]['name']}\n"
                                                            f"возраст: {ankets[add_info_for_bot['n']][0]['age']}\n"
                                                            f"Пол: {ankets[add_info_for_bot['n']][0]['gender_of_user']}\n"
                                                            f"Объявление: {ankets[add_info_for_bot['n']][0]['add_text_of_player']}\n",
                                   reply_markup=Keyboard.answer_kb())


async def player_info_form(id_of_chat: int):
    if add_info_for_bot["circle"] == 3.1 or add_info_for_bot["circle"] == 420:
        await bot.send_message(text="Как тебя зовут?", chat_id=id_of_chat)
    elif add_info_for_bot["circle"] == 4.1 or add_info_for_bot["circle"] == 421:
        await bot.send_message(text="Какого ты пола?", chat_id=id_of_chat, reply_markup=Keyboard.get_gender())
    elif add_info_for_bot["circle"] == 5.1 or add_info_for_bot["circle"] == 422:
        await bot.send_message(text="Сколько тебе лет?", chat_id=id_of_chat)
    elif add_info_for_bot["circle"] == 6.1 or add_info_for_bot["circle"] == 423:
        await bot.send_message(text="В каких жанрах ты играешь?", chat_id=id_of_chat,
                               reply_markup=Keyboard.get_genres())
    elif add_info_for_bot["circle"] == 7.1 or add_info_for_bot["circle"] == 424:
        await bot.send_message(text="Напиши текст о себе. Его будут видеть другие пользователи", chat_id=id_of_chat,
                               reply_markup=ReplyKeyboardRemove())


async def group_info_form(id_of_chat: int):
    if add_info_for_bot["circle"] == 0:
        add_info_for_bot["circle"] += 1
        await bot.send_message(text=f"Как называется твоя группа?",
                               chat_id=id_of_chat)
    elif add_info_for_bot["circle"] == 1 or add_info_for_bot["circle"] == 109:
        if add_info_for_bot["circle"] == 1:
            add_info_for_bot["circle"] += 1
            await bot.send_message(text=f"В каком жанре вы играете?",
                                   chat_id=id_of_chat, reply_markup=Keyboard.get_genres())
        else:
            await bot.send_message(text=f"В каком жанре вы играете?",
                                   chat_id=id_of_chat, reply_markup=Keyboard.get_genres())
    elif add_info_for_bot["circle"] == 2 or add_info_for_bot["circle"] == 108:
        if add_info_for_bot["circle"] == 2:
            add_info_for_bot["circle"] += 1
            await bot.send_message(text=f"У вас есть репетиционная база?",
                                   chat_id=id_of_chat, reply_markup=Keyboard.true_false_kb(), )
        else:
            await bot.send_message(text=f"У вас есть репетиционная база?",
                                   chat_id=id_of_chat, reply_markup=Keyboard.true_false_kb())
    elif add_info_for_bot["circle"] == 3:
        add_info_for_bot["circle"] += 1
        await bot.send_message(text=f"Пришли фото его будут видеть другие пользователи",
                               chat_id=id_of_chat)
    elif add_info_for_bot["circle"] == 4:
        add_info_for_bot["circle"] += 1
        await bot.send_message(text=f"Расскажите о группе",
                               chat_id=id_of_chat)


async def edit_form(id_of_chat: int):
    if add_info_for_bot["circle"] == 6:
        await bot.send_message(text="Что вы хотите изменить?", reply_markup=Keyboard.edit_group_form_kb(),
                               chat_id=id_of_chat)
    elif add_info_for_bot["circle"] == 11:
        await bot.send_message(text="Что вы хотите изменить?", chat_id=id_of_chat,
                               reply_markup=Keyboard.edit_finding_player_form_kb())
    elif add_info_for_bot["circle"] == 3.1:
        await bot.send_message(text="Что вы хотите изменить?", chat_id=id_of_chat,
                               reply_markup=Keyboard.edit_finding_group_form_kb())
    elif add_info_for_bot["circle"] == 8.1:
        await bot.send_message(text="Что вы хотите изменить?", chat_id=id_of_chat,
                               reply_markup=Keyboard.edit_about_player_form())


async def find_player_form(id_of_chat: int):
    if add_info_for_bot["circle"] == 6 or add_info_for_bot["circle"] == 222:
        if add_info_for_bot["circle"] == 6:
            add_info_for_bot["circle"] += 1
            await bot.send_message(text="Замечательно!\n"
                                        "Теперь поговорим о том, кого вы ищете\n"
                                        "Выберите пол музыканта", chat_id=id_of_chat,
                                   reply_markup=Keyboard.get_gender())
        else:
            await bot.send_message(text="Выберите пол музыканта", chat_id=id_of_chat,
                                   reply_markup=Keyboard.get_gender())
    elif add_info_for_bot["circle"] == 7 or add_info_for_bot["circle"] == 223:
        if add_info_for_bot["circle"] == 7:
            add_info_for_bot["circle"] += 1
            await bot.send_message(text="Теперь возраст", chat_id=id_of_chat)
            await bot.send_message(text="От скольки лет вы ищете музыканта?", chat_id=id_of_chat)
        else:
            await bot.send_message(text="От скольки лет вы ищете музыканта?", chat_id=id_of_chat)
    elif add_info_for_bot["circle"] == 8 or add_info_for_bot["circle"] == 224:
        if add_info_for_bot["circle"] == 8:
            add_info_for_bot["circle"] += 1
            await bot.send_message(text="До скольки лет вы ищете музыканта?", chat_id=id_of_chat)
        else:
            await bot.send_message(text="До скольки лет вы ищете музыканта?", chat_id=id_of_chat)
    elif add_info_for_bot["circle"] == 9 or add_info_for_bot["circle"] == 225:
        if add_info_for_bot["circle"] == 9:
            add_info_for_bot["circle"] += 1
            await bot.send_message(text="В каком жанре он должен играть?", chat_id=id_of_chat,
                                   reply_markup=Keyboard.get_genres())
        else:
            await bot.send_message(text="В каком жанре он должен играть?", chat_id=id_of_chat,
                                   reply_markup=Keyboard.get_genres())
    elif add_info_for_bot["circle"] == 10:
        add_info_for_bot["circle"] += 1
        await bot.send_message(text="Напишите само объявление. Его будут видеть пользователи", chat_id=id_of_chat,
                               reply_markup=ReplyKeyboardRemove())


async def find_group_form(id_of_chat: int):
    if add_info_for_bot["circle"] == 0 or add_info_for_bot["circle"] == 320:
        if add_info_for_bot["circle"] == 0:
            add_info_for_bot["circle"] += 1.1
            await bot.send_message(text=f"В каком жанре должна играть группа?",
                                   chat_id=id_of_chat, reply_markup=Keyboard.get_genres())
        else:
            await bot.send_message(text=f"В каком жанре должна играть группа?",
                                   chat_id=id_of_chat, reply_markup=Keyboard.get_genres())
    elif add_info_for_bot["circle"] == 1.1 or add_info_for_bot["circle"] == 321:
        if add_info_for_bot["circle"] == 1.1:
            add_info_for_bot["circle"] += 1
            await bot.send_message(text=f"Должна ли быть репетиционная база?",
                                   chat_id=id_of_chat, reply_markup=Keyboard.true_false_kb())
        else:
            await bot.send_message(text=f"Должна ли быть репетиционная база?",
                                   chat_id=id_of_chat, reply_markup=Keyboard.true_false_kb())


async def echo_group_blank(id_of_chat: int):
    await bot.send_photo(chat_id=id_of_chat, photo=about_group_info_form["photo_id"],
                         caption=f"Название группы: {about_group_info_form['group_name']}\n"
                                 f"Жанр: {', '.join(about_group_info_form['genre'])}\n"
                                 f"Наличие репетиционной базы: {about_group_info_form['repetition_base']}\n"
                                 f"О группе: {about_group_info_form['about_group']}\n\n"
                                 f"Всё правильно?", reply_markup=Keyboard.true_false_kb())


async def echo_finding_player_blank(id_of_chat):
    await bot.send_message(chat_id=id_of_chat, text=f"Кого ищешь: \n"
                                                    f"Пол: {finding_player_info_form['gender']}\n"
                                                    f"Возраст от {finding_player_info_form['age_range'][0]} "
                                                    f"до {finding_player_info_form['age_range'][1]}: \n"
                                                    f"Жанр: {', '.join(finding_player_info_form['genre_of_player'])}\n"
                                                    f"Текст объявления:\n {finding_player_info_form['add_text']}\n\n"
                                                    f"Всё правильно?", reply_markup=Keyboard.true_false_kb())


async def echo_finding_group_blank(id_of_chat):
    await bot.send_message(chat_id=id_of_chat, text=f"Кого ищешь: Группу\n"
                                                    f"Жанр: {', '.join(finding_group_info_form['genre_of_group'])}\n"
                                                    f"Наличие репетиционной базы: "
                                                    f"{finding_group_info_form['repetition_base_of_group']}\n\n"
                                                    f"Всё правильно?", reply_markup=Keyboard.true_false_kb())


async def echo_about_player_blank(id_of_chat):
    await bot.send_message(chat_id=id_of_chat, text=f"О себе: \n"
                                                    f"Имя: {about_player_info_form['name']}\n"
                                                    f"Пол: {about_player_info_form['gender_of_user']}\n"
                                                    f"Возраст: {about_player_info_form['age']}\n"
                                                    f"Твой жанр: {', '.join(about_player_info_form['genre_of_user'])}\n"
                                                    f"О себе:\n {(about_player_info_form['add_text_of_player'])}\n\n"
                                                    f"Всё правильно?", reply_markup=Keyboard.true_false_kb())


@dp.message_handler(commands=['start'])
async def bot_start(message: Message):
    await message.answer(text="awdaw" ,reply_markup=ReplyKeyboardRemove())
    if await check_user(message.from_user.id):
        await user_menu(message.from_user.id)
    else:
        await message.answer("Кого ты ищешь?", reply_markup=Keyboard.start_keyboard())


@dp.callback_query_handler()
async def start_callback(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if callback_query.data == "notify":
        add_info_for_bot["n"] = 0
        await notify(callback_query.from_user.id)
    elif callback_query.data == "newsfeed":
        await newsfeed(callback_query.from_user.id)
    elif callback_query.data == "user_menu":
        add_info_for_bot["n"] = 0
        await user_menu(callback_query.from_user.id)
    elif callback_query.data == "dislike":
        if not add_info_for_bot["last"]:
            await newsfeed(callback_query.from_user.id)
        else:
            pass
    elif callback_query.data == "ignore":
        if not add_info_for_bot["last"]:
            await notify(callback_query.from_user.id)
        else:
            pass
    elif callback_query.data == "like":
        if not add_info_for_bot["last"]:
            if await is_player(callback_query.from_user.id):
                await like_group(callback_query.from_user.id, add_info_for_bot["last_id"])
                await newsfeed(callback_query.from_user.id)
            else:
                await like_player(callback_query.from_user.id, add_info_for_bot["last_id"])
                await newsfeed(callback_query.from_user.id)
        else:
            if await is_player(callback_query.from_user.id):
                await like_group(callback_query.from_user.id, add_info_for_bot["last_id"])
            else:
                await like_player(callback_query.from_user.id, add_info_for_bot["last_id"])
    elif callback_query.data == "write":
        await bot.send_message(text=f"<a href='tg://user?id={add_info_for_bot['last_id']}'>Нажми,чтобы написать</a>", chat_id=callback_query.from_user.id,
                               parse_mode=ParseMode.HTML)
    elif callback_query.data == "group":
        await find_group_form(callback_query.from_user.id)
    elif callback_query.data == "musician":
        await group_info_form(callback_query.from_user.id)
    elif callback_query.data == "yes":
        if add_info_for_bot["circle"] == 3 or add_info_for_bot["circle"] == 108:
            about_group_info_form["repetition_base"] = "Да"
            if add_info_for_bot["circle"] == 3:
                await group_info_form(callback_query.from_user.id)
            else:
                add_info_for_bot["circle"] = 6
                await echo_group_blank(callback_query.from_user.id)
        elif add_info_for_bot["circle"] == 6:
            await find_player_form(callback_query.from_user.id)
        elif add_info_for_bot["circle"] == 2.1 or add_info_for_bot["circle"] == 321:
            if add_info_for_bot["circle"] == 2.1:
                add_info_for_bot["circle"] += 1
                finding_group_info_form["repetition_base_of_group"] = "Да"
                await echo_finding_group_blank(callback_query.from_user.id)
            else:
                finding_group_info_form["repetition_base_of_group"] = "Да"
                add_info_for_bot["circle"] = 3.1
                await echo_finding_group_blank(callback_query.from_user.id)
        elif add_info_for_bot["circle"] == 8.1:
            about_player_info_form["user_id"] = callback_query.from_user.id
            print(callback_query.from_user.id)                # id пользователя
            await add_player()
            add_info_for_bot["circle"] = 0
            await user_menu(callback_query.from_user.id)
        elif add_info_for_bot["circle"] == 11:
            about_player_info_form["user_id"] = callback_query.from_user.id  # id пользователя
            await add_group()
            add_info_for_bot["circle"] = 0
            await user_menu(callback_query.from_user.id)
        elif add_info_for_bot["circle"] == 3.1:
            await player_info_form(callback_query.from_user.id)
    elif callback_query.data == "no":
        if add_info_for_bot["circle"] == 3 or add_info_for_bot["circle"] == 108:
            about_group_info_form["repetition_base"] = "Нет"
            if add_info_for_bot["circle"] == 3:
                await group_info_form(callback_query.from_user.id)
            else:
                add_info_for_bot["circle"] = 6
                await echo_group_blank(callback_query.from_user.id)
        elif add_info_for_bot["circle"] == 6 or add_info_for_bot["circle"] == 11:
            await edit_form(callback_query.from_user.id)
        elif add_info_for_bot["circle"] == 2.1 or add_info_for_bot["circle"] == 321:
            if add_info_for_bot["circle"] == 2.1:
                add_info_for_bot["circle"] += 1
                finding_group_info_form["repetition_base_of_group"] = "Нет"
                await echo_finding_group_blank(callback_query.from_user.id)
            else:
                add_info_for_bot["circle"] = 3.1
                finding_group_info_form["repetition_base_of_group"] = "Нет"
                await echo_finding_group_blank(callback_query.from_user.id)
        elif add_info_for_bot["circle"] == 3.1:
            await edit_form(callback_query.from_user.id)
        elif add_info_for_bot["circle"] == 8.1:
            await edit_form(callback_query.from_user.id)
    elif callback_query.data == "back":
        if add_info_for_bot["circle"] == 6:
            await echo_group_blank(callback_query.from_user.id)
        elif add_info_for_bot["circle"] == 11:
            await echo_finding_player_blank(callback_query.from_user.id)
        elif add_info_for_bot["circle"] == 3:
            await echo_finding_group_blank(callback_query.from_user.id)
        elif add_info_for_bot["circle"] == 8.1:
            await echo_about_player_blank(callback_query.from_user.id)
    elif callback_query.data in about_group_info_form.keys():
        add_info_for_bot["circle"] = 111
        add_info_for_bot["request_for_edit"] = callback_query.data
        if callback_query.data == "photo_id":
            add_info_for_bot["circle"] = 110
            await bot.send_message(text="Отправьте новую картинку", chat_id=callback_query.from_user.id)
        elif callback_query.data == "repetition_base":
            add_info_for_bot["circle"] = 108
            await group_info_form(callback_query.from_user.id)
        elif callback_query.data == "genre":
            add_info_for_bot["circle"] = 109
            about_group_info_form["genre"].clear()
            await group_info_form(callback_query.from_user.id)
        else:
            await bot.send_message(text="Введите новый текст", chat_id=callback_query.from_user.id)
    elif callback_query.data in finding_player_info_form.keys():
        add_info_for_bot["request_for_edit"] = callback_query.data
        if callback_query.data == "gender":
            add_info_for_bot["circle"] = 222
            await find_player_form(callback_query.from_user.id)
        elif callback_query.data == "age_range":
            add_info_for_bot["circle"] = 223
            finding_player_info_form["age_range"].clear()
            await find_player_form(callback_query.from_user.id)
        elif callback_query.data == "genre_of_player":
            add_info_for_bot["circle"] = 225
            finding_player_info_form["genre_of_player"].clear()
            await find_player_form(callback_query.from_user.id)
        else:
            add_info_for_bot["circle"] = 226
            await bot.send_message(text="Введите новый текст", chat_id=callback_query.from_user.id)
    elif add_info_for_bot["circle"] == 222 or add_info_for_bot["circle"] == 7:
        finding_player_info_form["gender"] = callback_query.data
        if add_info_for_bot["request_for_edit"] == "":
            await find_player_form(callback_query.from_user.id)
        else:
            add_info_for_bot["request_for_edit"] = ""
            add_info_for_bot["circle"] = 11
            await echo_finding_player_blank(callback_query.from_user.id)
    elif callback_query.data == "genre_of_group":
        add_info_for_bot["circle"] = 320
        finding_group_info_form["genre_of_group"].clear()
        await find_group_form(callback_query.from_user.id)
    elif callback_query.data == "repetition_base_of_group":
        add_info_for_bot["circle"] = 321
        await find_group_form(callback_query.from_user.id)
    elif add_info_for_bot["circle"] == 4.1 or add_info_for_bot["circle"] == 421:
        if add_info_for_bot["circle"] == 4.1:
            add_info_for_bot["circle"] += 1
            about_player_info_form["gender_of_user"] = callback_query.data
            await player_info_form(callback_query.from_user.id)
        else:
            add_info_for_bot["circle"] = 8.1
            about_player_info_form["gender_of_user"] = callback_query.data
            await echo_about_player_blank(callback_query.from_user.id)
    elif callback_query.data == "name":
        add_info_for_bot["circle"] = 420
        await bot.send_message(text="Введите новое имя", chat_id=callback_query.from_user.id)
    elif callback_query.data == "gender_of_user":
        add_info_for_bot["circle"] = 421
        await player_info_form(callback_query.from_user.id)
    elif callback_query.data == "age":
        add_info_for_bot["circle"] = 422
        await bot.send_message(text="Введите новый возраст", chat_id=callback_query.from_user.id)
    elif callback_query.data == "genre_of_user":
        add_info_for_bot["circle"] = 423
        about_player_info_form["genre_of_user"].clear()
        await player_info_form(callback_query.from_user.id)
    elif callback_query.data == "add_text_of_player":
        add_info_for_bot["circle"] = 424
        await player_info_form(callback_query.from_user.id)


@dp.message_handler(content_types=['document', 'photo', 'text'])
async def handler(message: Message):
    if add_info_for_bot["circle"] == 4 or add_info_for_bot["circle"] == 110:
        if add_info_for_bot["circle"] == 4:
            if message.content_type == "photo":
                photos = message.photo
                new_id = photos[-1].file_id
                about_group_info_form["photo_id"] = new_id
                await group_info_form(message.from_user.id)
            else:
                await message.answer("Нам нужна картинка!")
        elif add_info_for_bot["circle"] == 110:
            if message.content_type == "photo":
                photos = message.photo
                new_id = photos[-1].file_id
                about_group_info_form["photo_id"] = new_id
                add_info_for_bot["request_for_edit"].clear()
                add_info_for_bot["circle"] = 6
                await echo_group_blank(message.from_user.id)
            else:
                await message.answer("Нам нужна картинка!")
    elif add_info_for_bot["circle"] == 1:
        about_group_info_form["group_name"] = message.text
        await group_info_form(message.from_user.id)
    elif add_info_for_bot["circle"] == 3:
        about_group_info_form["repetition_base"] = message.text
        await group_info_form(message.from_user.id)
    elif add_info_for_bot["circle"] == 5:
        about_group_info_form["about_group"] = message.text
        add_info_for_bot["circle"] += 1
        await echo_group_blank(message.from_user.id)
    elif add_info_for_bot["circle"] == 111:
        add_info_for_bot["circle"] = 6
        about_group_info_form[add_info_for_bot["request_for_edit"]] = message.text
        add_info_for_bot["request_for_edit"] = ""
        await echo_group_blank(message.from_user.id)
    elif add_info_for_bot["circle"] == 8 or add_info_for_bot["circle"] == 223:
        add_info_for_bot["request_for_edit"] = ""
        if add_info_for_bot["circle"] == 8:
            finding_player_info_form["age_range"].append(message.text)
            await find_player_form(message.from_user.id)
        else:
            finding_player_info_form["age_range"].append(message.text)
            add_info_for_bot["circle"] = 224
            await find_player_form(message.from_user.id)
    elif add_info_for_bot["circle"] == 9 or add_info_for_bot["circle"] == 224:
        if add_info_for_bot["circle"] == 9:
            finding_player_info_form["age_range"].append(message.text)
            await find_player_form(message.from_user.id)
        else:
            add_info_for_bot["circle"] = 11
            finding_player_info_form["age_range"].append(message.text)
            await echo_finding_player_blank(message.from_user.id)
    elif add_info_for_bot["circle"] == 11 or add_info_for_bot["circle"] == 226:
        add_info_for_bot["circle"] = 11
        add_info_for_bot["request_for_edit"] = ""
        finding_player_info_form["add_text"] = message.text
        await echo_finding_player_blank(message.from_user.id)
    elif add_info_for_bot["circle"] == 3.1 or add_info_for_bot["circle"] == 420:
        if add_info_for_bot["circle"] == 3.1:
            add_info_for_bot["circle"] += 1
            about_player_info_form["name"] = message.text
            await player_info_form(message.from_user.id)
        else:
            add_info_for_bot["circle"] = 8.1
            about_player_info_form["name"] = message.text
            await echo_about_player_blank(message.from_user.id)
    elif add_info_for_bot["circle"] == 5.1 or add_info_for_bot["circle"] == 422:
        if add_info_for_bot["circle"] == 5.1:
            add_info_for_bot["circle"] += 1
            about_player_info_form["age"] = int(message.text)
            await player_info_form(message.from_user.id)
        else:
            add_info_for_bot["circle"] = 8.1
            about_player_info_form["age"] = int(message.text)
            await echo_about_player_blank(message.from_user.id)
    elif add_info_for_bot["circle"] == 7.1 or add_info_for_bot["circle"] == 424:
        add_info_for_bot["circle"] = 8.1
        about_player_info_form["add_text_of_player"] = message.text
        await echo_about_player_blank(message.from_user.id)
    elif add_info_for_bot["circle"] == 2 or add_info_for_bot["circle"] == 109:
        if add_info_for_bot["circle"] == 2:
            if message.text != "Закончить":
                add_info_for_bot["circle"] = 1
                about_group_info_form["genre"].append(message.text)
                await group_info_form(message.from_user.id)
            else:
                add_info_for_bot["request_for_edit"] = ""
                await group_info_form(message.from_user.id)
        else:
            if message.text != "Закончить":
                about_group_info_form["genre"].append(message.text)
                await group_info_form(message.from_user.id)
            else:
                add_info_for_bot["request_for_edit"] = ""
                add_info_for_bot["circle"] = 6
                await echo_group_blank(message.from_user.id)
    elif add_info_for_bot["circle"] == 10 or add_info_for_bot["circle"] == 225:
        if add_info_for_bot["circle"] == 10:
            if message.text != "Закончить":
                add_info_for_bot["circle"] -= 1
                finding_player_info_form["genre_of_player"].append(message.text)
                await find_player_form(message.from_user.id)
            else:
                await find_player_form(message.from_user.id)
        else:
            if message.text != "Закончить":
                finding_player_info_form["genre_of_player"].append(message.text)
                await find_player_form(message.from_user.id)
            else:
                add_info_for_bot["circle"] = 11
                await echo_finding_player_blank(message.from_user.id)
    elif add_info_for_bot["circle"] == 1.1 or add_info_for_bot["circle"] == 320:
        if add_info_for_bot["circle"] == 1.1:
            if message.text != "Закончить":
                add_info_for_bot["circle"] -= 1.1
                finding_group_info_form["genre_of_group"].append(message.text)
                await find_group_form(message.from_user.id)
            else:
                await find_group_form(message.from_user.id)
        else:
            if message.text != "Закончить":
                finding_group_info_form["genre_of_group"].append(message.text)
                await find_group_form(message.from_user.id)
            else:
                add_info_for_bot["circle"] = 3.1
                await echo_finding_group_blank(message.from_user.id)
    elif add_info_for_bot["circle"] == 6.1 or add_info_for_bot["circle"] == 423:
        if add_info_for_bot["circle"] == 6.1:
            if message.text != "Закончить":
                about_player_info_form["genre_of_user"].append(message.text)
                await player_info_form(message.from_user.id)
            else:
                add_info_for_bot["circle"] += 1
                await player_info_form(message.from_user.id)
        else:
            if message.text != "Закончить":
                about_player_info_form["genre_of_user"].append(message.text)
                await player_info_form(message.from_user.id)
            else:
                add_info_for_bot["circle"] = 8.1
                await echo_about_player_blank(message.from_user.id)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
