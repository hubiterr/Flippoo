from pyrogram import Client, filters, types
from pyrogram.errors.exceptions.bad_request_400 import UserAdminInvalid, BadRequest
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import asyncio
import configparser as cp
from crud import *
from icecream import ic



#  ________  _________  ________  ________  _________   
# |\   ____\|\___   ___\\   __  \|\   __  \|\___   ___\ 
# \ \  \___|\|___ \  \_\ \  \|\  \ \  \|\  \|___ \  \_| 
#  \ \_____  \   \ \  \ \ \   __  \ \   _  _\   \ \  \  
#   \|____|\  \   \ \  \ \ \  \ \  \ \  \\  \|   \ \  \ 
#     ____\_\  \   \ \__\ \ \__\ \__\ \__\\ _\    \ \__\
#    |\_________\   \|__|  \|__|\|__|\|__|\|__|    \|__|
#    \|_________|                                                 
cfg = cp.ConfigParser()
cfg.read('config.ini')
print('Config Readed')
token_bot = cfg.get('API_KEYS', 'tokenBot')
api_hash = cfg.get('API_KEYS', 'apiHash')
api_id = int(cfg.get('API_KEYS', 'apiId'))
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=token_bot)


#  ________  ________  ________   ________ ___  ________     
# |\   ____\|\   __  \|\   ___  \|\  _____\\  \|\   ____\    
# \ \  \___|\ \  \|\  \ \  \\ \  \ \  \__/\ \  \ \  \___|    
#  \ \  \    \ \  \\\  \ \  \\ \  \ \   __\\ \  \ \  \  ___  
#   \ \  \____\ \  \\\  \ \  \\ \  \ \  \_| \ \  \ \  \|\  \ 
#    \ \_______\ \_______\ \__\\ \__\ \__\   \ \__\ \_______\
#     \|_______|\|_______|\|__| \|__|\|__|    \|__|\|_______|                                          
mute_delay = int(cfg.get('SETTING', 'mute_delay'))
sticker_spam = {}
gif_spam = {}
global_cfg = {}
rules = cfg.get('SETTING', 'rule_link')


# ________      ___    ___ ________  ___       _______   ________      
#|\   ____\    |\  \  /  /|\   ____\|\  \     |\  ___ \ |\   ____\     
#\ \  \___|    \ \  \/  / | \  \___|\ \  \    \ \   __/|\ \  \___|_    
# \ \  \        \ \    / / \ \  \    \ \  \    \ \  \_|/_\ \_____  \   
#  \ \  \____    \/  /  /   \ \  \____\ \  \____\ \  \_|\ \|____|\  \  
#   \ \_______\__/  / /      \ \_______\ \_______\ \_______\____\_\  \ 
#    \|_______|\___/ /        \|_______|\|_______|\|_______|\_________\
#             \|___|/                                      \|_________|                                                                                                      
@app.on_message(filters.sticker & filters.group)
async def handle_sticker(client, msg):
    await handle_media_spam(client, msg, sticker_spam, "стикеров")

@app.on_message(filters.animation & filters.group)
async def handle_gif(client, msg):
    await handle_media_spam(client, msg, gif_spam, "гифок")


#  ________ ___  ___  ________   ________ _________  ___  ________  ________   ________      
# |\  _____\\  \|\  \|\   ___  \|\   ____\\___   ___\\  \|\   __  \|\   ___  \|\   ____\     
# \ \  \__/\ \  \\\  \ \  \\ \  \ \  \___\|___ \  \_\ \  \ \  \|\  \ \  \\ \  \ \  \___|_    
#  \ \   __\\ \  \\\  \ \  \\ \  \ \  \       \ \  \ \ \  \ \  \\\  \ \  \\ \  \ \_____  \   
#   \ \  \_| \ \  \\\  \ \  \\ \  \ \  \____   \ \  \ \ \  \ \  \\\  \ \  \\ \  \|____|\  \  
#    \ \__\   \ \_______\ \__\\ \__\ \_______\  \ \__\ \ \__\ \_______\ \__\\ \__\____\_\  \ 
#     \|__|    \|_______|\|__| \|__|\|_______|   \|__|  \|__|\|_______|\|__| \|__|\_________\
#                                                                                \|_________|
    
#спам триггер
async def handle_media_spam(client, msg, spam_dict, media_type):
    user_id = msg.from_user.id
    if user_id in spam_dict:
        spam_dict[user_id] += 1
    else:
        spam_dict[user_id] = 1

    if spam_dict[user_id] > 3:
        try:
            until_date = (datetime.now() + timedelta(seconds=mute_delay)).replace(microsecond=0)
            await client.restrict_chat_member(msg.chat.id, user_id, permissions=types.ChatPermissions(), until_date=until_date)
            await msg.reply(f"Вы отправили слишком много {media_type} подряд и были замучены на {mute_delay//60} минут.")
            spam_dict[user_id] = 0
        except:
            await msg.reply("Вы хоть админ или модератор, но спамить лучше не надо")
            spam_dict[user_id] = 0

    await asyncio.sleep(1)

# градация увеличения мута за спам
async def nmap(decimal):
    gradations = {
        0.1: 300,
        0.5: 1800,
        0.9: 40000
        # Добавьте любые другие значения, если необходимо
    }
    
    # Сортируем карту градаций по ключам (десятичным числам)
    sorted_gradations = sorted(gradations.items())
    
    # Если десятичное число меньше первого в карте градаций,
    # возвращаем значение первого ключа
    if decimal < sorted_gradations[0][0]:
        return sorted_gradations[0][1]
    
    # Если десятичное число больше последнего в карте градаций,
    # возвращаем значение последнего ключа
    if decimal > sorted_gradations[-1][0]:
        return sorted_gradations[-1][1]
    
    # Иначе проходим по карте градаций и находим соответствующий интервал
    for i in range(len(sorted_gradations) - 1):
        if sorted_gradations[i][0] <= decimal < sorted_gradations[i+1][0]:
            # Интерполируем между двумя значениями в карте градаций
            fraction = (decimal - sorted_gradations[i][0]) / (sorted_gradations[i+1][0] - sorted_gradations[i][0])
            return int(sorted_gradations[i][1] + fraction * (sorted_gradations[i+1][1] - sorted_gradations[i][1]))

# рефактор даты
async def ref_date(date_string):
    date_formats = [
        "%d-%m-%Y", "%d/%m/%Y", "%d.%m.%Y",
        "%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d",
        "%d %b %Y", "%d %B %Y",
        "%b %d %Y", "%B %d %Y",
        "%d %b %y", "%d %B %y",
        "%b %d %y", "%B %d %y"
    ]

    formatted_date = None
    for date_format in date_formats:
        try:
            date_obj = datetime.strptime(date_string, date_format)
            formatted_date = date_obj.strftime("%d.%m.%Y")
            break
        except ValueError:
            continue
    
    if formatted_date is None:
        return "Невозможно распознать формат даты."
    else:
        return formatted_date

#текущее время
async def cur_date():
    current_date = datetime.now()
    formatted_date = current_date.strftime("%d.%m.%Y %H:%M")
    return formatted_date

#выдача бана
async def ban_member(client, chat_id, user_id, reason='Без причины.'):
    try:
        await client.ban_chat_member(chat_id, user_id)
        await client.send_message(chat_id, f"[Виновник](tg://user?id={user_id})\nБыл забанен по причине:\n{reason}")
    except UserAdminInvalid as e:
        print(f"ERROR: {e}")
        await client.send_message(chat_id, f"[Админ](tg://user?id={user_id}) является администратором!")
    except BadRequest as e:
        print(f"ERROR: {e}")
        await client.send_message(chat_id, f"Не могу заблокировать [Виновника](tg://user?id={user_id})!")

# Функция для разбана пользователя
async def unban_member(client, chat_id, user_id, reason=''):
    await client.unban_chat_member(chat_id, user_id)
    await client.send_message(chat_id, "Пользователь разблокирован" + f"\n\nПо причине:\n{reason}" if reason != '' else "")

# Функция для выдачи мута на время (в секундах)
async def mute_user(client, chat_id, user_id, duration):
    permissions = types.ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_polls=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False,
        can_change_info=False,
        can_invite_users=False,
        can_pin_messages=False
    )
    until_date = datetime.now() + timedelta(seconds=duration)
    await client.restrict_chat_member(chat_id, user_id, until_date=until_date, permissions=permissions)

# Функция для снятия мута с пользователя
async def unmute_user(client, chat_id, user_id):
    permissions = types.ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_polls=False,
        can_send_other_messages=True,
        can_add_web_page_previews=False,
        can_change_info=False,
        can_invite_users=True,
        can_pin_messages=False
    )
    await client.restrict_chat_member(chat_id, user_id, permissions=permissions)

async def upd_cfg(cfg):
    with open('config.ini', 'w') as configfile:
        cfg.write(configfile)

async def get_admin_members(chat_id):
    admin_members = []
    owner = []

    async for member in app.get_chat_members(chat_id):
        if member.status == ChatMemberStatus.ADMINISTRATOR:
            admin_members.append(member)
        elif member.status == ChatMemberStatus.OWNER:
            owner.append(member)
    return admin_members, owner

# ___       __   _______   ___       ________  ________  _____ ______   _______      
#|\  \     |\  \|\  ___ \ |\  \     |\   ____\|\   __  \|\   _ \  _   \|\  ___ \     
#\ \  \    \ \  \ \   __/|\ \  \    \ \  \___|\ \  \|\  \ \  \\\__\ \  \ \   __/|    
# \ \  \  __\ \  \ \  \_|/_\ \  \    \ \  \    \ \  \\\  \ \  \\|__| \  \ \  \_|/__  
#  \ \  \|\__\_\  \ \  \_|\ \ \  \____\ \  \____\ \  \\\  \ \  \    \ \  \ \  \_|\ \ 
#   \ \____________\ \_______\ \_______\ \_______\ \_______\ \__\    \ \__\ \_______\
#    \|____________|\|_______|\|_______|\|_______|\|_______|\|__|     \|__|\|_______|
                                                                                                                                       
@app.on_message(filters.new_chat_members)
async def greet_new_members(client, msg):
    user = MAIN.get_user_data(msg.from_user.id)
    if msg.from_user.is_bot:
        return
    if user:
        await msg.reply_text(f"Приветствую тебя в <b>{msg.chat.title}</b>!\nКажется я тебя видела раньше в этом чате, с возвращением^^\nПожалуйста, ознакомься с <a href='{rules}'>правилами чата</a> ^^")
    else:
        await msg.reply_text(f"Приветствую тебя в <b>{msg.chat.title}</b>!\nПожалуйста, ознакомься с <a href='{rules}'>правилами чата</a> ^^")

#  _____ ______   ________  ___  ________           ___       ________  ________  ________   
# |\   _ \  _   \|\   __  \|\  \|\   ___  \        |\  \     |\   __  \|\   __  \|\   __  \  
# \ \  \\\__\ \  \ \  \|\  \ \  \ \  \\ \  \       \ \  \    \ \  \|\  \ \  \|\  \ \  \|\  \ 
#  \ \  \\|__| \  \ \   __  \ \  \ \  \\ \  \       \ \  \    \ \  \\\  \ \  \\\  \ \   ____\
#   \ \  \    \ \  \ \  \ \  \ \  \ \  \\ \  \       \ \  \____\ \  \\\  \ \  \\\  \ \  \___|
#    \ \__\    \ \__\ \__\ \__\ \__\ \__\\ \__\       \ \_______\ \_______\ \_______\ \__\   
#     \|__|     \|__|\|__|\|__|\|__|\|__| \|__|        \|_______|\|_______|\|_______|\|__|                                                                           
@app.on_message(filters.group)
async def main_group(client, msg):
    if not msg or msg.from_user.is_bot:
        return
    
    if not str(msg.chat.id) == cfg.get('SETTING', 'main'):
        return
    chat_id = msg.chat.id
    cmd = msg.text.lower().split(" ")
    user = MAIN.get_user_data(msg.from_user.id)
    if not user:
        MAIN.register(
            id=msg.from_user.id, 
            nick=msg.from_user.username, 
            name=msg.from_user.first_name + "" if not msg.from_user.last_name else msg.from_user.last_name,
            bdate = "", 
            jdate = await cur_date(),
        )
    else:
        if user[0]['rate'] >= 2:
            if cmd[0] in ['/set', 'set', 'сет'] and len(cmd) >= 2:
                if cmd[1] in ['td', "mutetime", "мут"]:
                    if cmd[2].isdigit():
                        global mute_delay
                        mute_delay = int(cmd[2]) * 60
                        await client.send_message(chat_id, f"Время мута при спаме установлено - {mute_delay//60} минут")
                    else:
                        await client.send_message(chat_id, "Укажите время в минутах! (число '5')")
                elif cmd[1] in ["devchat", "закулисье"]:
                    cfg.set('SETTING', 'dev', str(msg.chat.id))
                    await msg.reply_text("чат ЗАКУЛИСЬЕ обновлен! Удачного дня!")
                    await upd_cfg(cfg)
                elif cmd[1] in ["mainchat", "основа"]:
                    cfg.set('SETTING', 'main', str(msg.chat.id))
                    await msg.reply_text("чат ОСНОВА обновлен! Удачного дня!")
                    await upd_cfg(cfg)
            elif cmd[0] in ['id', "ид"]:
                await client.send_message(chat_id, f"Ваш айди - <code>{msg.from_user.id}</code>")
                await client.send_message(chat_id, f"Чат айди - <code>{msg.chat.id}</code>")           
            elif cmd[0] in ['ban', "бан"]:
                if len(cmd) >= 1:
                    reason = " ".join(cmd[1:])
                else:
                    reason = False
                if msg.reply_to_message.from_user:
                    if reason:
                        await ban_member(client, chat_id, msg.reply_to_message.from_user.id, reason=reason)
                    else:
                        await ban_member(client, chat_id, msg.reply_to_message.from_user.id)
                else:
                    await client.send_message(chat_id, "Для бана необходимо ответить на сообщение пользователя!")
            elif cmd[0] in ['unban', 'анбан']:
                if len(cmd) >= 1:
                    reason = " ".join(cmd[1:])
                else:
                    reason = False
                if msg.reply_to_message.from_user:
                    if reason:
                        await unban_member(client, chat_id, msg.reply_to_message.from_user.id, reason=reason)
                    else:
                        await unban_member(client, chat_id, msg.reply_to_message.from_user.id)
                else:
                    await client.send_message(chat_id, "Для разблокировки необходимо ответить на сообщение пользователя!")
            elif cmd[0] in ["мут", 'mute']:
                if msg.reply_to_message.from_user:
                    if len(cmd) == 2:
                        if cmd[1].isdigit():
                            mute_d = int(cmd[1])
                            await mute_user(client, chat_id, msg.reply_to_message.from_user.id, mute_d*60)
                            await msg.reply_text(f"[Пользователь](tg://user?id={msg.reply_to_message.from_user.id}) получил мут на {round(mute_d, 1)} минут")
                        else:
                            await msg.reply_text("Указано не правильная длительность мута! (Целое число в минутах)")
                    else:
                        await mute_user(client, chat_id, msg.reply_to_message.from_user.id, mute_delay)
                        await msg.reply_text(f"[Пользователь](tg://user?id={msg.reply_to_message.from_user.id}) получил мут на {round(mute_delay/60, 1)} минут")
                else:
                    await msg.reply_text("Ответьте на чье то сообщение для мута!")
            elif cmd[0] in ["говори", 'speak', 'спик', 'анмут']:
                if msg.reply_to_message.from_user:
                    await unmute_user(client, chat_id, msg.reply_to_message.from_user.id)
                    await msg.reply_text(f"Вы дали [Пользователю](tg://user?id={msg.reply_to_message.from_user.id}) возможность говорить")
                else:
                    await msg.reply_text("Ответьте на чье то сообщение для анмута!")
        if cmd[0] in ["/админы", '!админы']:
            admin_members, owner = await get_admin_members(chat_id)
            text = "\nГлава\n"
            for own in owner:
                us += f"{own.user.first_name} {own.user.last_name if own.user.last_name else ''}\n"
                text += f"[{us}](tg://user?id={own.id})"
            text += "\nМодераторы Чата\n"
            for admin in admin_members:
                us += f"{admin.user.first_name} {admin.user.last_name if admin.user.last_name else ''}\n"
                text += f"[{us}](tg://user?id={admin.id})"

            await client.send_message(chat_id, text)
        elif cmd[0] in ["рапорт", "репорт", "report", 'raport'] and str(msg.chat.id) == cfg.get('SETTING', 'main'):
            if msg.reply_to_message:
                try:
                    if global_cfg[msg.reply_to_message.from_user.id]['rt'] >= 1:
                        pass
                except:
                    global_cfg[msg.reply_to_message.from_user.id] = {"rt": 1}

                inline_keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("Бан", callback_data=f"ban_{msg.reply_to_message.from_user.id}")],
                        [InlineKeyboardButton("Игнор", callback_data=f"denied_")]
                ])
                text = f'''
Поступил репорт на сообщение:
<code>{msg.reply_to_message.text}</code>

[Виновник](tg://user?id={msg.reply_to_message.from_user.id})

[Кто жалуется](tg://user?id={msg.from_user.id})
'''
                await client.send_message(cfg.get('SETTING', 'dev'), text, reply_markup=inline_keyboard)
                await client.send_message(chat_id, 'рапорт будет расмотрен модераторами!')
            else:
                await client.send_message(chat_id, "Необходимо ответить на чье либо сообщение для репорта")
        elif cmd[0] == 'пинг':
            await msg.reply_text('ПОНГ!')

@app.on_message(filters.private)
async def main_private(client, msg):
    if msg.from_user.is_bot:
        return
    
    chat_id = msg.chat.id
    cmd = msg.text.lower().split(" ")
    if cmd[0] in ['login', 'логин'] and len(cmd) == 2:
        if cmd[1] == cfg.get('SETTING', 'dev_pass'):
            cfg.set('SETTING', 'developer', str(msg.from_user.id))
            await upd_cfg(cfg)
            await client.send_message(chat_id, f"Приветствую вас Создатель!")
        else:
            try:
                if global_cfg[msg.from_user.id]['dev_try'] != 0:
                    global_cfg[msg.from_user.id]['dev_try'] -= 1
            except:
                global_cfg[msg.from_user.id] = {"dev_try": 2}
            if global_cfg[msg.from_user.id]['dev_try']:
                await client.send_message(chat_id, f"Неверный пароль!!!\n Осталось попыток -{global_cfg[msg.from_user.id]['dev_try']}")
    if str(msg.from_user) == cfg.get('SETTING', 'developer'):
        if cmd[0] in ["rate", "рейт"] and len(cmd) == 2:
            MAIN.update_user(msg.from_user.id, {"rate": int(cmd[1])})
            await msg.reply_text("Уровень изменен!")

#  ________  ________  ___       ___       ________  ________  ________  ___  __    ________      
# |\   ____\|\   __  \|\  \     |\  \     |\   __  \|\   __  \|\   ____\|\  \|\  \ |\   ____\     
# \ \  \___|\ \  \|\  \ \  \    \ \  \    \ \  \|\ /\ \  \|\  \ \  \___|\ \  \/  /|\ \  \___|_    
#  \ \  \    \ \   __  \ \  \    \ \  \    \ \   __  \ \   __  \ \  \    \ \   ___  \ \_____  \   
#   \ \  \____\ \  \ \  \ \  \____\ \  \____\ \  \|\  \ \  \ \  \ \  \____\ \  \\ \  \|____|\  \  
#    \ \_______\ \__\ \__\ \_______\ \_______\ \_______\ \__\ \__\ \_______\ \__\\ \__\____\_\  \ 
#     \|_______|\|__|\|__|\|_______|\|_______|\|_______|\|__|\|__|\|_______|\|__| \|__|\_________\
#                                                                                     \|_________|
@app.on_callback_query()
async def callback_query(client, query):
    data = query.data.split("_")
    if data[0] == "ban":
        text_data = query.message.text + '\n\n ЮЗЕР ЗАБЛОКИРОВАН'
        await query.message.edit_text(text_data)
        await ban_member(client, int(cfg.get('SETTING', 'main')), int(data[1]), 'Рапорт')

    elif data[0] == "denied":
        text_data = query.message.text + '\n\n РАПОРТ ОТКЛОНЕН'
        await query.message.edit_text(text_data)                                                          


if __name__ == "__main__":                                                               
    print("Start bot!")
    try:
        app.run()
    except KeyboardInterrupt as e:
        print(e)
else:
    print("! NOT IMPORTABLE MAIN FILE !")
    quit()