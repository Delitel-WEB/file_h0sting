# -*- coding: utf-8 -*-
# Created by Delitel

from aiogram import types
from bot import db


def main_keyboard():
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

	keyboard.add("Мои файлы 💾")
	#keyboard.add("Популярные файлы ⚙️")

	return keyboard

def my_files(user_id):
	files = db.get_files(user_id)
	files.reverse() # разварачиваем список
	keyboard = types.InlineKeyboardMarkup()


	if not files:
		keyboard_1 = types.InlineKeyboardButton(text= "Файлы не найдены 😬", callback_data="add_file")
		keyboard_2 = types.InlineKeyboardButton(text = "Добавить файл ➕", callback_data='add_file')
		keyboard_3 = types.InlineKeyboardButton(text = "Назад⤴️", callback_data = "go_home")
		keyboard.add(keyboard_1)
		keyboard.add(keyboard_2)
		keyboard.add(keyboard_3)

	else:

		keyboard_2 = types.InlineKeyboardButton(text = "Назад⤴️", callback_data = "go_home")
		keyboard_3 = types.InlineKeyboardButton(text = "⬅️", callback_data = "go_left")
		keyboard_4 = types.InlineKeyboardButton(text = "➡️", callback_data = "go_right")
		keyboard_6 = types.InlineKeyboardButton(text = "Добавить файл ➕", callback_data='add_file')


		counter = 0 #СЧЁТЧИК
		status, = db.get_status(user_id)
		status = int(status.split("|")[1])

		count_files = len(files)
		begin_count = status - 7

		remain_files = count_files - begin_count

		if remain_files <= 0 and status != 7:
			db.set_status(user_id, f"count_page|{status - 7}|my_files")
			keyboard = None
			keyboard.add(keyboard_3, keyboard_2, keyboard_4)
		else:
			for i in files[begin_count:status]:
				if counter == status:
					break
				else:																											
					keyboard_5 = types.InlineKeyboardButton(text = f"{i[4]}", callback_data= f"files_button|{i[0]}")
					keyboard.add(keyboard_5)
					counter += 1

			keyboard.add(keyboard_3, keyboard_2, keyboard_4)
			keyboard.add(keyboard_6)

	return keyboard


def remove_relpy_keyb():
	keyboard = types.ReplyKeyboardRemove()

	return keyboard

def dont_work_keyb():
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add("Воспользуйтесь клавиатурой сверху")

	return keyboard

def go_back():
	keyboard = types.InlineKeyboardMarkup()
	keyboard_1 = types.InlineKeyboardButton(text = "Назад⤴️", callback_data = "go_home")
	keyboard.add(keyboard_1)

	return keyboard

def acces_keyboard(id_, upd):
	keyboard = types.InlineKeyboardMarkup()

	keyboard_1 = types.InlineKeyboardButton(text="Все", callback_data=f"access_buttons|all|{id_}|{upd}")
	keyboard_2 = types.InlineKeyboardButton(text="Я", callback_data=f"access_buttons|me|{id_}|{upd}")
	#keyboard_1 = types.InlineKeyboardButton(text="Некторые люди", callback_data=f"access_buttons|some_people|{id_}")
	keyboard.add(keyboard_1, keyboard_2)

	return keyboard

def files_keyb(id_):
	keyboard = types.InlineKeyboardMarkup()
	keyboard_1 = types.InlineKeyboardButton(text = "Переименовать файл 🔡", callback_data=f"file_impact|rename_file|{id_}")
	keyboard_2 = types.InlineKeyboardButton(text= "Настройки просмотра 👁", callback_data=f"file_impact|view_settings|{id_}")
	keyboard_3 = types.InlineKeyboardButton(text = "Удалить файл ❌", callback_data=f"file_impact|delete_file|{id_}")
	keyboard_4 = types.InlineKeyboardButton(text = "Назад⤴️", callback_data = "go_home")


	keyboard.add(keyboard_1)
	keyboard.add(keyboard_2)
	keyboard.add(keyboard_3)
	keyboard.add(keyboard_4)

	return keyboard

def view_settings(id_):
	keyboard = types.InlineKeyboardMarkup()
	keyboard_1 = types.InlineKeyboardButton(text="👁‍🗨 Ограничить доступ", callback_data=f"file_impact|limit_access|{id_}")
	keyboard_2 = types.InlineKeyboardButton(text="🔗 Пересоздать ссылку", callback_data=f"file_impact|recopy_link|{id_}")
	keyboard_3 = types.InlineKeyboardButton(text = "Назад к файлу⤴️", callback_data= f"files_button|{id_}")
	keyboard.add(keyboard_1)
	keyboard.add(keyboard_2)
	keyboard.add(keyboard_3)

	return keyboard


def go_back_to_file(id_):
	keyboard = types.InlineKeyboardMarkup()
	keyboard_1 = types.InlineKeyboardButton(text = "Назад к файлу⤴️", callback_data= f"files_button|{id_}")
	keyboard.add(keyboard_1)

	return keyboard

def deep_link_keyb(id_, me=False):
	keyboard = types.InlineKeyboardMarkup()
	if me == True:
		keyboard_1 = types.InlineKeyboardButton(text = "Переименовать файл 🔡", callback_data=f"file_impact|rename_file|{id_}")
		keyboard_2 = types.InlineKeyboardButton(text= "Настройки просмотра 👁", callback_data=f"file_impact|view_settings|{id_}")
		keyboard_3 = types.InlineKeyboardButton(text = "Удалить файл ❌", callback_data=f"file_impact|delete_file|{id_}")
		keyboard.add(keyboard_1)
		keyboard.add(keyboard_2)
		keyboard.add(keyboard_3)

	else:

		keyboard_1 = types.InlineKeyboardButton(text="➕ Добавить в мои файлы", callback_data=f"file_impact|add_my_files|{id_}")
		keyboard.add(keyboard_1)


	keyboard_4 = types.InlineKeyboardButton(text = "Назад⤴️", callback_data = "go_home")
	keyboard.add(keyboard_4)

	return keyboard

def admin_keyboard():
	keyboard = types.InlineKeyboardMarkup()

	keyboard_1 = types.InlineKeyboardButton(text = "Просмотр файлов", callback_data="view_files")
	keyboard_2 = types.InlineKeyboardButton(text = "Выгрузка файлов", callback_data="download_files")

	keyboard.add(keyboard_1)
	keyboard.add(keyboard_2)

	return keyboard










