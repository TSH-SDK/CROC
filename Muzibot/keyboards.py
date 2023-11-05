from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from data import finding_player_info_form, finding_group_info_form, about_player_info_form, add_info_for_bot


class Keyboard:

    @staticmethod
    def start_keyboard():
        inline_btn_1 = InlineKeyboardButton('Ищу группу', callback_data='group')
        inline_btn_2 = InlineKeyboardButton('Ищу музыканта', callback_data='musician')
        inline_kb1 = InlineKeyboardMarkup().row(inline_btn_1, inline_btn_2)
        return inline_kb1

    @staticmethod
    def true_false_kb():
        inline_btn_1 = InlineKeyboardButton("Да", callback_data="yes")
        inline_btn_2 = InlineKeyboardButton("Нет", callback_data="no")
        inline_kb2 = InlineKeyboardMarkup().row(inline_btn_1, inline_btn_2)
        return inline_kb2

    @staticmethod
    def edit_group_form_kb():
        inline_btn_1 = InlineKeyboardButton("Название группы", callback_data="group_name")
        inline_btn_2 = InlineKeyboardButton("Жанр", callback_data="genre")
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
        inline_btn_3 = InlineKeyboardButton("Жанр", callback_data="genre_of_player")
        inline_btn_4 = InlineKeyboardButton("Текст объявления", callback_data="add_text")
        inline_btn_5 = InlineKeyboardButton("Назад", callback_data="back")
        inline_kb_6 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4, inline_btn_5)

        return inline_kb_6

    @staticmethod
    def edit_finding_group_form_kb():
        inline_btn_1 = InlineKeyboardButton("Жанр", callback_data="genre_of_group")
        inline_btn_2 = InlineKeyboardButton("Наличие репетиционной базы", callback_data="repetition_base_of_group")
        inline_btn_3 = InlineKeyboardButton("Назад", callback_data="back")
        inline_kb_7 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2, inline_btn_3)

        return inline_kb_7

    @staticmethod
    def get_gender():
        inline_kb4 = InlineKeyboardMarkup()
        inline_btn_1 = InlineKeyboardButton("Парень", callback_data="Парень")
        inline_btn_2 = InlineKeyboardButton("Девушка", callback_data="Девушка")
        if add_info_for_bot["circle"] != 4.1 and add_info_for_bot["circle"] != 421:
            inline_btn_3 = InlineKeyboardButton("Без разницы", callback_data="Без разницы")
            inline_kb4.add(inline_btn_3)
        inline_kb4.add(inline_btn_1, inline_btn_2)
        return inline_kb4

    @staticmethod
    def get_genres():
        inline_kb5 = InlineKeyboardMarkup(row_width=2)
        with open("genres.txt", "r", encoding="utf-8") as f:
            text = f.read()
            for i, j in enumerate(text.split("\n")):
                inline_btn = InlineKeyboardButton(j, callback_data=f"{j}")
                inline_kb5.add(inline_btn)
            if len(finding_player_info_form["genre_of_player"]) != 0 or len(finding_group_info_form["genre_of_group"]) != 0:
                add_but = InlineKeyboardButton("Закончить", callback_data="finish")
                inline_kb5.add(add_but)
            elif len("about_group_info_form") != 0:
                add_but = InlineKeyboardButton("Закончить", callback_data="finish")
                inline_kb5.add(add_but)
            return inline_kb5

    @staticmethod
    def edit_about_player_form():
        inline_btn_1 = InlineKeyboardButton("Имя", callback_data="name")
        inline_btn_2 = InlineKeyboardButton("Пол", callback_data="gender_of_user")
        inline_btn_3 = InlineKeyboardButton("Возраст", callback_data="age")
        inline_btn_4 = InlineKeyboardButton("Жанр", callback_data="genre_of_user")
        inline_btn_5 = InlineKeyboardButton("Текст объявления", callback_data="add_text_of_player")
        inline_btn_6 = InlineKeyboardButton("Назад", callback_data="back")
        inline_kb_9 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2, inline_btn_3, inline_btn_4, inline_btn_5,
                                                 inline_btn_6)
        return inline_kb_9
