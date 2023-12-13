from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from data import add_info_for_bot

from db_module import check_genres, check_find_genres, group_age, check_false


class Keyboard:

    @staticmethod
    def start_keyboard():
        inline_btn_1 = InlineKeyboardButton('Ищу группу', callback_data='group')
        inline_btn_2 = InlineKeyboardButton('Ищу музыканта', callback_data='musician')
        inline_kb1 = InlineKeyboardMarkup().row(inline_btn_1, inline_btn_2)
        return inline_kb1

    @staticmethod
    def true_false_kb():
        inline_btn_1 = InlineKeyboardButton("Да", callback_data="Да")
        inline_btn_2 = InlineKeyboardButton("Нет", callback_data="Нет")
        inline_kb2 = InlineKeyboardMarkup().row(inline_btn_1, inline_btn_2)
        return inline_kb2

    @staticmethod
    def true_edit_kb():
        inline_btn_1 = InlineKeyboardButton("Да", callback_data="Да")
        inline_btn_2 = InlineKeyboardButton("Изменить", callback_data="Изменить")
        inline_kb14 = InlineKeyboardMarkup().row(inline_btn_1, inline_btn_2)
        return inline_kb14

    @staticmethod
    def edit_group_form_kb():
        inline_btn_1 = InlineKeyboardButton("Название группы", callback_data="group_name")
        inline_btn_2 = InlineKeyboardButton("Жанр", callback_data="genres")
        inline_btn_3 = InlineKeyboardButton("Наличие репетиционной базы", callback_data="repetition_base")
        inline_btn_4 = InlineKeyboardButton("О группе", callback_data="about_group")
        inline_btn_5 = InlineKeyboardButton("Картинка", callback_data="photo_id")
        inline_btn_6 = InlineKeyboardButton("Назад", callback_data="back")
        inline_kb3 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4, inline_btn_5,
                                                inline_btn_6)
        return inline_kb3

    @staticmethod
    def edit_finding_player_form_kb():
        inline_btn_1 = InlineKeyboardButton("Пол", callback_data="gender")
        inline_btn_2 = InlineKeyboardButton("Возраст", callback_data="age_range")
        inline_btn_3 = InlineKeyboardButton("Жанр", callback_data="fp_genres")
        inline_btn_4 = InlineKeyboardButton("Текст объявления", callback_data="add_text")
        inline_btn_5 = InlineKeyboardButton("Назад", callback_data="back")
        inline_kb_6 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4, inline_btn_5)

        return inline_kb_6

    @staticmethod
    def edit_finding_group_form_kb():
        inline_btn_1 = InlineKeyboardButton("Жанр", callback_data="fg_genres")
        inline_btn_2 = InlineKeyboardButton("Наличие репетиционной базы", callback_data="repetition_base_of_group")
        inline_btn_3 = InlineKeyboardButton("Назад", callback_data="back")
        inline_kb_7 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2, inline_btn_3)

        return inline_kb_7

    @staticmethod
    async def get_gender(user_id):
        inline_kb4 = InlineKeyboardMarkup()
        inline_btn_1 = InlineKeyboardButton("Парень", callback_data="Парень")
        inline_btn_2 = InlineKeyboardButton("Девушка", callback_data="Девушка")
        if await group_age(user_id):
            inline_btn_3 = InlineKeyboardButton("Без разницы", callback_data="Без разницы")
            inline_kb4.add(inline_btn_3)
        inline_kb4.add(inline_btn_1, inline_btn_2)
        return inline_kb4

    @staticmethod
    async def get_genres(user_id):
        reply_kb5 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        button1 = KeyboardButton("Фолк-музыка")
        button2 = KeyboardButton("Кантри")
        button3 = KeyboardButton("Блюз")
        button4 = KeyboardButton("Ритм-н-блюз")
        button5 = KeyboardButton("Джаз")
        button6 = KeyboardButton("Классическая музыка")
        button7 = KeyboardButton("Электронная музыка")
        button8 = KeyboardButton("Рок")
        button9 = KeyboardButton("Метал")
        button10 = KeyboardButton("Хип-хоп")
        button11 = KeyboardButton("Регги")
        button12 = KeyboardButton("Фанк")
        button13 = KeyboardButton("Соул")
        button14 = KeyboardButton("Диско")
        button15 = KeyboardButton("Поп-музыка")
        check_box = ["fp_genres", "fg_genres"]
        if await check_genres(user_id) and await check_false(user_id) == "genres":
            add_but = KeyboardButton("Закончить")
            reply_kb5.row(add_but)
        elif await check_find_genres(user_id) and await check_false(user_id) in check_box:
            add_but = KeyboardButton("Закончить")
            reply_kb5.row(add_but)
        reply_kb5.row(button1, button2, button3)
        reply_kb5.row(button4, button5, button6)
        reply_kb5.row(button7,button8, button9)
        reply_kb5.row(button10, button11, button12)
        reply_kb5.row(button13, button14, button15)

        return reply_kb5

    @staticmethod
    def edit_about_player_form():
        inline_btn_1 = InlineKeyboardButton("Имя", callback_data="name")
        inline_btn_2 = InlineKeyboardButton("Пол", callback_data="gender_of_user")
        inline_btn_3 = InlineKeyboardButton("Возраст", callback_data="age")
        inline_btn_4 = InlineKeyboardButton("Жанр", callback_data="genres")
        inline_btn_5 = InlineKeyboardButton("Фото", callback_data="photo_id")
        inline_btn_6 = InlineKeyboardButton("Текст объявления", callback_data="add_text_of_player")
        inline_btn_7 = InlineKeyboardButton("Назад", callback_data="back")
        inline_kb_9 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4, inline_btn_5,
                                                 inline_btn_6, inline_btn_7)
        return inline_kb_9

    @staticmethod
    def user_menu():
        inline_btn_1 = InlineKeyboardButton("Уведомления", callback_data="notify")
        inline_btn_2 = InlineKeyboardButton("Изменить\n анкету", callback_data="change_ank")
        inline_btn_3 = InlineKeyboardButton("Лента\n объявлений", callback_data="newsfeed")
        inline_kb_10 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2, inline_btn_3)
        return inline_kb_10

    @staticmethod
    def like_dislike(user_id):
        inline_btn_1 = InlineKeyboardButton("Лайк❤️", callback_data=f"like/{user_id}")
        inline_btn_2 = InlineKeyboardButton("Дизлайк", callback_data="dislike")
        if not add_info_for_bot["last"]:
            inline_btn_3 = InlineKeyboardButton("Выйти в меню", callback_data="user_menu")
            inline_kb_11 = InlineKeyboardMarkup(row_width=2).add(inline_btn_1, inline_btn_2, inline_btn_3)
        else:
            inline_kb_11 = InlineKeyboardMarkup(row_width=2).add(inline_btn_1, inline_btn_2)
        return inline_kb_11

    @staticmethod
    def back_to_menu():
        inline_btn = InlineKeyboardButton("Выйти в меню", callback_data="user_menu")
        inline_kb_12 = InlineKeyboardMarkup().add(inline_btn)
        return inline_kb_12

    @staticmethod
    def answer_kb():
        inline_btn_1 = InlineKeyboardButton("Написать", callback_data="write")
        inline_btn_2 = InlineKeyboardButton("Игнорировать", callback_data="ignore")
        if not add_info_for_bot["last"]:
            inline_btn_3 = InlineKeyboardButton("Выйти в меню", callback_data="user_menu")
            inline_kb_13 = InlineKeyboardMarkup(row_width=2).add(inline_btn_1, inline_btn_2, inline_btn_3)
        else:
            inline_kb_13 = InlineKeyboardMarkup(row_width=2).add(inline_btn_1, inline_btn_2)
        return inline_kb_13

    @staticmethod
    def accept_kb():
        inline_btn_1 = InlineKeyboardButton("Да", callback_data="change")
        inline_btn_2 = InlineKeyboardButton("Нет", callback_data="no_change")
        inline_kb14 = InlineKeyboardMarkup().row(inline_btn_1, inline_btn_2)
        return inline_kb14
