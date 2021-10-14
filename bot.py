# -*- coding: utf-8 -*-
# Created by Delitel

from aiogram import Bot, executor, Dispatcher
import keyboard, cfg
from db import SQLither
from aiogram.utils.deep_linking import get_start_link
from aiogram.utils import exceptions
import datetime
import random



bot = Bot(cfg.token)
dp = Dispatcher(bot)
db = SQLither("main_db.db")
chars = "134567890qwertyuiopasdfghjklzxcvbnm"

def extract_unik_code(text): # Получение кода из deep_link
    if not text.split()[0] == "/start":
        return None
    else:
        return text.split()[1] if len(text.split()) > 1 else None

async def deleted_messages(user_id): # Очистка чата
	messages_delete = db.get_deletions_messages(user_id)
	for i in messages_delete:
		try:
			await bot.delete_message(user_id, i[1])
		except exceptions.MessageToDeleteNotFound:
			pass
		except exceptions.MessageCantBeDeleted:
			pass
		db.delete_deletions_message(i[1])

async def access_(user_id, id_, form, f_, upd=None):
	if form == "photo":
		mess_id = await bot.send_photo(
			user_id,
			id_,
			caption ="Выберите доступ для файла:",
			reply_markup=keyboard.acces_keyboard(f_, upd)
			)
		db.add_delete_message(user_id, mess_id.message_id)
	elif form == "video":
		mess_id = await bot.send_video(
			user_id,
			id_,
			caption="Выберите доступ для файла:",
			reply_markup=keyboard.acces_keyboard(f_, upd)
			)
		db.add_delete_message(user_id, mess_id.message_id)
	elif form == "audio":
		mess_id = await bot.send_audio(
			user_id,
			id_,
			caption="Выберите доступ для файла:",
			reply_markup=keyboard.acces_keyboard(f_, upd)
			)
		db.add_delete_message(user_id, mess_id.message_id)
	elif form == "animation":
		mess_id = await bot.send_animation(
			user_id,
			id_,
			caption="Выберите доступ для файла:",
			reply_markup=keyboard.acces_keyboard(f_, upd)
			)
		db.add_delete_message(user_id, mess_id.message_id)
	elif form == "document":
		mess_id = await bot.send_document(
			user_id,
			id_,
			caption="Выберите доступ для файла:",
			reply_markup=keyboard.acces_keyboard(f_, upd)
			)
		db.add_delete_message(user_id, mess_id.message_id)


@dp.message_handler(content_types=["photo"]) #Принятие Фото
async def photo_handler(message):
	user_id = message.chat.id
	status, = db.get_status(user_id)
	await bot.delete_message(user_id, message.message_id)
	if message:
		if status == "upload_file":
			file_id = message["photo"][-1]["file_id"]
			time_upload = datetime.datetime.now()
			file_name = f"photo{time_upload}"
			form = "photo"
			link_ = "file2"
			for i in range(40):
				link_ += random.choice(chars)
			db.add_file(user_id, file_id, time_upload, file_name, form, link_)
			f = db.get_file(user_id, file_id)
			await access_(user_id, file_id, form, f[0])


@dp.message_handler(content_types=["video"]) # Принятие видео
async def video_handler(message):
	user_id = message.chat.id
	status, = db.get_status(user_id)
	await bot.delete_message(user_id, message.message_id)
	if message:
		if status == "upload_file":
			file_id = message["video"]["file_id"]
			time_upload = datetime.datetime.now()
			file_name = f"video{time_upload}"
			form = "video"
			link_ = "file2"
			for i in range(40):
				link_ += random.choice(chars)
			db.add_file(user_id, file_id, time_upload, file_name, form, link_)
			f = db.get_file(user_id, file_id)
			await access_(user_id, file_id, form, f[0])


@dp.message_handler(content_types=["audio"]) # ПРИНЯТИЕ АУДИО
async def audio_handler(message):
	user_id = message.chat.id
	status, = db.get_status(user_id)
	await bot.delete_message(user_id, message.message_id)
	if message:
		if status == "upload_file":
			file_id = message["audio"]["file_id"]
			time_upload = datetime.datetime.now()
			file_name = f"audio{time_upload}"
			form = "audio"
			link_ = "file2"
			for i in range(40):
				link_ +=  random.choice(chars)
			db.add_file(user_id, file_id, time_upload, file_name, form, link_)
			f = db.get_file(user_id, file_id)
			await access_(user_id, file_id, form, f[0])

@dp.message_handler(content_types=["animation"])# ПРИНЯТИЕ АНИМАЦИЙ
async def photo_handler(message):
	user_id = message.chat.id
	status, = db.get_status(user_id)
	await bot.delete_message(user_id, message.message_id)
	if message:
		if status == "upload_file":
			file_id = message["animation"]["file_id"]
			time_upload = datetime.datetime.now()
			file_name = message["animation"]["file_name"]
			form = "animation"
			link_ = "file2"
			for i in range(40):
				link_ += random.choice(chars)
			db.add_file(user_id, file_id, time_upload, file_name, form, link_)
			f = db.get_file(user_id, file_id)
			await access_(user_id, file_id, form, f[0])

@dp.message_handler(content_types=["document"]) # ПРИНЯТИЕ ДОКУМЕНТОВ
async def photo_handler(message):
	user_id = message.chat.id
	status, = db.get_status(user_id)
	await bot.delete_message(user_id, message.message_id)
	if message:
		if status == "upload_file":
			file_id = message["document"]["file_id"]
			time_upload = datetime.datetime.now()
			file_name = message["document"]["file_name"]
			form = "document"
			link_ = "file2"
			for i in range(40):
				link_ += random.choice(chars)
			db.add_file(user_id, file_id, time_upload, file_name, form, link_)
			f = db.get_file(user_id, file_id)
			await access_(user_id, file_id, form, f[0])




@dp.message_handler(content_types=["text"])
async def message_handler(message):
	user_id = message.chat.id #user_id Пользователя

	code = extract_unik_code(message.text)

	if not db.exists_user_id(user_id):
		db.add_user_id(user_id)

	status, = db.get_status(user_id)

	if code:
		if code.split("2")[0] == "file":
			file = db.get_file_byLink(code)
			if not file:
				await deleted_messages(user_id)
				mess_id = await message.answer(
					"<b>Файл не найден!</b>",
					parse_mode="html",
					reply_markup=keyboard.main_keyboard()
					)
				db.add_delete_message(user_id, mess_id.message_id)
			else:
				await deleted_messages(user_id)
				if file[5] == "me":
					mess_id = await message.answer(
					"<b>Файл не найден!</b>",
					parse_mode="html",
					reply_markup=keyboard.main_keyboard()
					)
					db.add_delete_message(user_id, mess_id.message_id)
				else:
					form = file[6]
					if file[1] == user_id:
						if form == "photo":
							mess_id = await bot.send_photo(
								user_id,
								file[2],
								caption=f"💻 Просмотр файла",
								reply_markup=keyboard.deep_link_keyb(file[0], me=True)
								)
							db.add_delete_message(user_id, mess_id.message_id)
						elif form == "video":
							mess_id = await bot.send_video(
								user_id,
								file[2],
								caption=f"💻 Просмотр файла",
								reply_markup=keyboard.deep_link_keyb(file[0], me=True)
								)
							db.add_delete_message(user_id, mess_id.message_id)
						elif form == "audio":
							mess_id = await bot.send_audio(
								user_id,
								file[2],
								caption=f"💻 Просмотр файла",
								reply_markup=keyboard.deep_link_keyb(file[0], me=True)
								)
							db.add_delete_message(user_id, mess_id.message_id)
						elif form == "animation":
							mess_id = await bot.send_animation(
								user_id,
								file[2],
								caption=f"💻 Просмотр файла",
								reply_markup=keyboard.deep_link_keyb(file[0], me=True)
								)
							db.add_delete_message(user_id, mess_id.message_id)
						elif form == "document":
							mess_id = await bot.send_document(
								user_id,
								file[2],
								caption=f"💻 Просмотр файла",
								reply_markup=keyboard.deep_link_keyb(file[0], me=True)
								)
							db.add_delete_message(user_id, mess_id.message_id)


					else:
						if form == "photo":
							mess_id = await bot.send_photo(
								user_id,
								file[2],
								caption=f"💻 Просмотр файла",
								reply_markup=keyboard.deep_link_keyb(file[0], me=False)
								)
							db.add_delete_message(user_id, mess_id.message_id)
						elif form == "video":
							mess_id = await bot.send_video(
								user_id,
								file[2],
								caption=f"💻 Просмотр файла",
								reply_markup=keyboard.deep_link_keyb(file[0], me=False)
								)
							db.add_delete_message(user_id, mess_id.message_id)
						elif form == "audio":
							mess_id = await bot.send_audio(
								user_id,
								file[2],
								caption=f"💻 Просмотр файла",
								reply_markup=keyboard.deep_link_keyb(file[0], me=False)
								)
							db.add_delete_message(user_id, mess_id.message_id)
						elif form == "animation":
							mess_id = await bot.send_animation(
								user_id,
								file[2],
								caption=f"💻 Просмотр файла",
								reply_markup=keyboard.deep_link_keyb(file[0], me=False)
								)
							db.add_delete_message(user_id, mess_id.message_id)
						elif form == "document":
							mess_id = await bot.send_document(
								user_id,
								file[2],
								caption=f"💻 Просмотр файла",
								reply_markup=keyboard.deep_link_keyb(file[0], me=False)
								)
							db.add_delete_message(user_id, mess_id.message_id)



	if message.text == "/start":
		mess_id = await message.answer(
			"<b>Добро пожаловать в бесплатный файлообменник в телеграмме!</b>\n\n"
			"Здесь вы можете загружать <b>любые</b> свои файлы весом до <b>2-ух ГБ</b> абсолютно <i>бесплатно</i>!",
			reply_markup=keyboard.main_keyboard(),
			parse_mode="html"
			)
		await bot.delete_message(user_id, message.message_id)
		db.add_delete_message(user_id, mess_id.message_id)

	elif message.text == "/adm":
		if db.exists_admin(user_id):
			mess_id = await message.answer("Доступ получен!", reply_markup=keyboard.admin_keyboard())
			await bot.delete_message(user_id, message.message_id)
			await deleted_messages(user_id)
			db.add_delete_message(user_id, mess_id.message_id)
		else:
			mess_id = await message.answer("Доступ запрещён!")
			await bot.delete_message(user_id, message.message_id)
			await deleted_messages(user_id)			
			db.add_delete_message(user_id, mess_id.message_id)

	elif message.text == "/version":
		mess_id = await message.answer("Стабильная версия бота", reply_markup=keyboard.go_back())
		await bot.delete_message(user_id, message.message_id)
		await deleted_messages(user_id)			
		db.add_delete_message(user_id, mess_id.message_id)

	elif message.text == "/id":
		await message.answer(f"Ваш id: <code>{user_id}</code>", parse_mode="html")




	elif message.text == "Мои файлы 💾":
		await bot.delete_message(user_id, message.message_id)
		db.set_status(user_id, "count_page|7|my_files")
		mess_id = await message.answer("🗄", reply_markup= keyboard.dont_work_keyb())
		mess_id_2 = await message.answer("Список ваших файлов:", reply_markup=keyboard.my_files(user_id))
		db.add_delete_message(user_id, mess_id.message_id)
		db.add_delete_message(user_id, mess_id_2.message_id)

	elif message.text == "Воспользуйтесь клавиатурой сверху":
		try:
			await bot.delete_message(user_id, message.message_id)
		except exceptions.MessageToDeleteNotFound:
			pass
		except exceptions.MessageCantBeDeleted:
			pass

	elif status.split("|")[0] == "rename_file":
		db.update_name_file(status.split("|")[1], message.text)
		db.set_status(user_id, 0)
		await bot.delete_message(user_id, message.message_id)
		db.set_status(user_id, "count_page|7|my_files")
		mess_id = await message.answer("🗄", reply_markup= keyboard.dont_work_keyb())
		mess_id_2 = await message.answer("Список ваших файлов:", reply_markup=keyboard.my_files(user_id))
		await deleted_messages(user_id)
		db.add_delete_message(user_id, mess_id.message_id)
		db.add_delete_message(user_id, mess_id_2.message_id)

	else:
		await bot.delete_message(user_id, message.message_id)










@dp.callback_query_handler()
async def qury_handler(call):
	user_id = call.message.chat.id
	status, = db.get_status(user_id)
	if call.message:
		if call.data == "go_left":
			count = int(status.split("|")[1])
			obj = status.split("|")[2]

			if obj == "my_files":
				if count == 7:
					await bot.answer_callback_query(
						callback_query_id = call.id,
						text = "Вы на самой первой странице!",
						show_alert = False
						)
				else:
					db.set_status(user_id, f"count_page|{count - 7}|my_files")
					try:
						await bot.edit_message_text(
							"<b>Список Файлов 📁:</b>",
							user_id,
							call.message.message_id,
							reply_markup = keyboard.my_files(user_id),
							parse_mode="html"
							)
					except:
						await bot.edit_message_text(
							"<b>Список Файлов 📂:</b>",
							user_id,
							call.message.message_id,
							reply_markup = keyboard.my_files(user_id),
							parse_mode="html"
							)
		elif call.data == "go_right":
			count = int(status.split("|")[1])
			obj = status.split("|")[2]

			if obj == "my_files":
				db.set_status(user_id, f"count_page|{count + 7}|my_files")
				try:
					await bot.edit_message_text(
						"<b>Список Файлов 📁:</b>",
						user_id,
						call.message.message_id,
						reply_markup = keyboard.my_files(user_id),
						parse_mode="html"
						)
				except AttributeError:
					await bot.answer_callback_query(
						callback_query_id = call.id,
						text = "Вы на последней странице!",
						show_alert = False
						)
				except MessageNotModified:
					await bot.edit_message_text(
						"<b>Список Файлов 📂:</b>",
						user_id,
						call.message.message_id,
						reply_markup = keyboard.my_files(user_id),
						parse_mode="html"
						)

		elif call.data == "go_home":
			mess_id = await call.message.answer(
				"<b>Вы в главном меню!</b>",
				parse_mode="html",
				reply_markup=keyboard.main_keyboard()
				)
			await deleted_messages(user_id)
			db.add_delete_message(user_id, mess_id.message_id)

		elif call.data == "add_file":
			db.set_status(user_id, "upload_file")
			await deleted_messages(user_id)
			mess_id = await call.message.answer(
				"Загрузите ваш файл!",
				reply_markup=keyboard.go_back()
				)
			await deleted_messages(user_id)
			db.add_delete_message(user_id, mess_id.message_id)


		elif call.data.split("|")[0] == "files_button":
			file = db.get_file_byID(call.data.split("|")[1])
			form = file[6]
			link = await get_start_link(file[7])
			await deleted_messages(user_id)
			if form == "photo":
				mess_id = await bot.send_photo(
					user_id,
					file[2],
					caption=f"⚙️ Настройки файла\n\nСсылка на файл:\n{link}",
					reply_markup=keyboard.files_keyb(file[0])
					)
				db.add_delete_message(user_id, mess_id.message_id)
			elif form == "video":
				mess_id = await bot.send_video(
					user_id,
					file[2],
					caption=f"⚙️ Настройки файла\n\nСсылка на файл:\n{link}",
					reply_markup=keyboard.files_keyb(file[0])
					)
				db.add_delete_message(user_id, mess_id.message_id)
			elif form == "audio":
				mess_id = await bot.send_audio(
					user_id,
					file[2],
					caption=f"⚙️ Настройки файла\n\nСсылка на файл:\n{link}",
					reply_markup=keyboard.files_keyb(file[0])
					)
				db.add_delete_message(user_id, mess_id.message_id)
			elif form == "animation":
				mess_id = await bot.send_animation(
					user_id,
					file[2],
					caption=f"⚙️ Настройки файла\n\nСсылка на файл:\n{link}",
					reply_markup=keyboard.files_keyb(file[0])
					)
				db.add_delete_message(user_id, mess_id.message_id)
			elif form == "document":
				mess_id = await bot.send_document(
					user_id,
					file[2],
					caption=f"⚙️ Настройки файла\n\nСсылка на файл:\n{link}",
					reply_markup=keyboard.files_keyb(file[0])
					)
				db.add_delete_message(user_id, mess_id.message_id)



		elif call.data.split("|")[0] == "access_buttons":
			db.update_access_data(call.data.split("|")[2], call.data.split("|")[1])
			if call.data.split("|")[3] == "None":
				await bot.answer_callback_query(
					callback_query_id=call.id,
					text="Файл успешно загружен!",
					show_alert=True
					)
				mess_id = await call.message.answer(
					"<b>Вы в главном меню!</b>",
					parse_mode="html",
					reply_markup=keyboard.main_keyboard()
					)
			else:
				await bot.answer_callback_query(
					callback_query_id=call.id,
					text="Доступ к просмотру успешно обновлён!",
					show_alert=True
					)
				mess_id = await call.message.answer(
					"<b>Ваши файлы:</b>",
					parse_mode="html",
					reply_markup=keyboard.my_files(user_id)
					)


			await deleted_messages(user_id)
			db.add_delete_message(user_id, mess_id.message_id)

		elif call.data.split("|")[0] == "file_impact":
			file = db.get_file_byID(call.data.split("|")[2])
			form = file[6]
			if call.data.split("|")[1] == "rename_file":
				await deleted_messages(user_id)
				mess_id = await call.message.answer(
					"🔤 Введите новое название файла:",
					reply_markup=keyboard.go_back_to_file(file[0])
					)
				db.add_delete_message(user_id, mess_id.message_id)
				db.set_status(user_id, f"rename_file|{file[0]}")
			elif call.data.split("|")[1] == "delete_file":
				db.delete_file(file[0])
				await bot.answer_callback_query(
					callback_query_id=call.id,
					text="Файл успешно удалён!",
					show_alert=True
				)
				await deleted_messages(user_id)
				db.set_status(user_id, "count_page|7|my_files")
				mess_id = await call.message.answer("🗄", reply_markup= keyboard.dont_work_keyb())
				mess_id_2 = await call.message.answer("Список ваших файлов:", reply_markup=keyboard.my_files(user_id))
				db.add_delete_message(user_id, mess_id.message_id)
				db.add_delete_message(user_id, mess_id_2.message_id)

			elif call.data.split("|")[1] == "view_settings":
				await deleted_messages(user_id)
				mess_id = await call.message.answer(
					"Настройки просмотра 👁",
					reply_markup=keyboard.view_settings(file[0])
					)
				db.add_delete_message(user_id, mess_id.message_id)

			elif call.data.split("|")[1] == "limit_access":
				await deleted_messages(user_id)
				await access_(user_id, file[2], file[6], file[0], upd=True)
			elif call.data.split("|")[1] == "recopy_link":
				link_ = "file2"
				for i in range(40):
					link_ += random.choice(chars)
				db.update_link(file[0], link_)
				await bot.answer_callback_query(
					callback_query_id=call.id,
					text="Ссылка успешно обновлена!",
					show_alert=True
					)
				await deleted_messages(user_id)
				mess_id = await call.message.answer(
					"Настройки просмотра 👁",
					reply_markup=keyboard.view_settings(file[0])
					)
				db.add_delete_message(user_id, mess_id.message_id)
			elif call.data.split("|")[1] == "add_my_files":



				file_id = file[2]
				time_upload = datetime.datetime.now()
				file_name = file[4]
				form = file[6]
				link_ = "file2"
				for i in range(40):
					link_ += random.choice(chars)
				db.add_file(user_id, file_id, time_upload, file_name, form, link_)
				f = db.get_file_byLink(link_)
				await deleted_messages(user_id)
				await access_(user_id, file_id, form, f[0])













if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)