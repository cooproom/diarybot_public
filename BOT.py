from vkwave.bots import SimpleLongPollBot, Keyboard, ButtonColor
from vkwave.bots.storage.types import Key, Dumper, Loader
from pyowm.utils.config import get_default_config
from vkwave.types.bot_events import BotEventType
from vkwave.bots.storage.storages import Storage
from datetime import timedelta
from datetime import date
from datetime import datetime
from db import DataBase
from config import Config
import threading
import schedule
import asyncio
import string
import vk_api
import pyowm
import json
import time
conf = Config()
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = pyowm.OWM(conf.weather, config_dict)
mgr = owm.weather_manager()
db = DataBase
bot = SimpleLongPollBot(tokens=[conf.vk_api], group_id=200632750)


def jobe():
    vk_session = vk_api.VkApi(
        token=conf.vk_api)
    vk = vk_session.get_api()
    print("-отдельный процесс-"+str(datetime.now().time()))
    from db import DataBase
    dba = DataBase
    while True:
        data = str(datetime.now().date())
        datear = dba.load(dba, data, 'alarmt')
        timer = datetime.now().time().hour
        for nam in datear:
            if int(timer) >= int(nam[3]):
                vk.messages.send(random_id=0, peer_id=int(
                    nam[0]), message="✏НАПОМИНАНИЕ!\n"+nam[3]+":00\n"+nam[1])
                dba.delete(dba, nam[0], 'alarms', nam[1])
                print('-отправлено-напоминание-' +
                      str(nam[0])+'-'+str(datetime.now().time()))
        time.sleep(2)


job_thread = threading.Thread(target=jobe)
job_thread.start()

kbdate = Keyboard()
kbdate.add_text_button(text="Сегодня", color=ButtonColor.POSITIVE)
kbdate.add_text_button(text="Завтра", color=ButtonColor.POSITIVE)
kbdate.add_text_button(text="Послезавтра", color=ButtonColor.POSITIVE)
kbdate.add_row()
kbdate.add_text_button(text='Назад', color=ButtonColor.PRIMARY)

kbald = Keyboard()
kbald.add_text_button(text="09:00", color=ButtonColor.POSITIVE)
kbald.add_text_button(text="12:00", color=ButtonColor.POSITIVE)
kbald.add_text_button(text="15:00", color=ButtonColor.POSITIVE)
kbald.add_text_button(text="18:00", color=ButtonColor.POSITIVE)
kbald.add_row()
kbald.add_text_button(text="21:00", color=ButtonColor.POSITIVE)
kbald.add_text_button(text="23:00", color=ButtonColor.POSITIVE)
kbald.add_text_button(text="03:00", color=ButtonColor.POSITIVE)
kbald.add_text_button(text="06:00", color=ButtonColor.POSITIVE)
kbald.add_row()
kbald.add_text_button(text='Назад', color=ButtonColor.PRIMARY)


kbb = Keyboard()
kbb.add_text_button(text='Назад', color=ButtonColor.PRIMARY)

kbs = Keyboard()
kbs.add_text_button(text='На завтра', color=ButtonColor.PRIMARY)
kbs.add_text_button(text='Назад', color=ButtonColor.PRIMARY)

kbm = Keyboard()
kbm.add_text_button(text="Заметки", color=ButtonColor.PRIMARY)
kbm.add_text_button(text="Напоминания", color=ButtonColor.PRIMARY)
kbm.add_text_button(text="Сводка", color=ButtonColor.PRIMARY)

keephelp = 'Напишите заметку. Чтобы удалить заметку напишите\n "/номера через запятую"'
alarmhelp = 'Напишите напоминание. Чтобы удалить напоминание напишите\n "/номера через запятую"'
alhelplist = {}


@bot.message_handler(bot.text_contains_filter('/'))
async def delete(event: bot.SimpleBotEvent):
    user_id = event.object.object.message.peer_id
    status = db.load(db, user_id, 'status')
    if status[0][1] == 'keeps' or status[0][1] == 'alarms':
        text = event.object.object.message.text
        counter = ['']
        for u in text:
            if u.isdigit():
                counter[len(counter) - 1] += u
            else:
                counter.append('')
        l = db.load(db, user_id, status[0][1])
    for u in counter:
        if u.isdigit():
            try:
                name = l[int(u) - 1][1]
                db.delete(db, user_id, status[0][1], name)
                if status[0][1] == 'keeps':
                    text = 'Заметка удалена'
                elif status[0][1] == 'alarms':
                    text = 'Напоминание удалено'
                await event.answer(text + '\n')

            except:
                continue


@bot.message_handler(bot.text_filter(["заметки", '1']))
async def keeps(event: bot.SimpleBotEvent):
    user_id = event.object.object.message.peer_id
    print('-команда-заметки-'+str(user_id)+'-'+str(datetime.now().time()))
    load = db.load(db, user_id, 'keeps')
    text = 'Ваши заметки:\n'
    i = 1
    for item in load:
        text += str(i) + '. ' + item[1] + ' - ' + item[2] + '\n'
        i += 1
    if len(load) == 0:
        text = "Новых заметок нет"
    db.update(db, user_id, 'status', {'screen': 'keeps'})
    await event.answer(text + '\n' + keephelp, keyboard=kbb.get_keyboard())


@bot.message_handler(bot.text_filter(["напоминания", '2']))
async def alarms(event: bot.SimpleBotEvent):
    user_id = event.object.object.message.peer_id
    print('-команда-напоминания-'+str(user_id)+'-'+str(datetime.now().time()))
    load = db.load(db, user_id, 'alarms')
    text = 'Ваши напоминания:\n'
    i = 1
    for item in load:
        text += str(i) + '. ' + str(item[1]) + \
            ' - ' + item[2] + ' в ' + item[3] + ':00\n'
        i += 1
    if len(load) == 0:
        text = "Новых напоминаний нет"
    db.update(db, user_id, 'status', {'screen': 'alarms'})
    await event.answer(text + '\n' + alarmhelp, keyboard=kbb.get_keyboard())


@bot.message_handler(bot.text_filter(["сводка", "4"]))
async def sum(event: bot.SimpleBotEvent):
    user_id = event.object.object.message.peer_id
    print('-команда-сводка-'+str(user_id)+'-'+str(datetime.now().time()))
    db.update(db, user_id, 'status', {'screen': 'sum'})
    await event.answer(f"Это сводка на сегодня\nОна покажет вам самое важное на сегодня", keyboard=kbb.get_keyboard())
    weather = ""
    data = str(datetime.now().date())
    load = db.load(db, data, 'alarmt')
    text = 'Напоминания на сегодня:\n'
    i = 1
    for item in load:
        if str(user_id) == str(item[0]):
            text += str(i) + '. ' + str(item[1]) + \
                ' - ' + item[2] + ' в ' + item[3] + ':00\n'
        i += 1
    if len(load) == 0:
        text = "На сегодня нет напоминаний"
    city = "Вологда"
    observation = mgr.weather_at_place(city)
    w = observation.weather
    weather = 'В городе '+city+" " + \
        str(int(w.temperature('celsius')['temp'])
            )+'°C, '+str(w.detailed_status)
    await event.answer(text + '\n' + weather, keyboard=kbb.get_keyboard())


@bot.message_handler(bot.text_filter(["главная", "0", "назад"]))
async def main(event: bot.SimpleBotEvent):
    @bot.message_handler(bot.text_contains_filter(''))
    async def saver(event: bot.SimpleBotEvent):
        user_id = event.object.object.message.peer_id
        status = db.load(db, user_id, 'status')
        if status[0][1] == 'keeps':
            text = event.object.object.message.text
            data = datetime.now().date()
            db.save(db, user_id, 'keeps', {'text': text, 'data': str(data)})
            await event.answer('Заметка сохранена')
            user_id = event.object.object.message.peer_id
            db.update(db, user_id, 'status', {'screen': 'keeps'})
            load = db.load(db, user_id, 'keeps')
            text = 'Ваши заметки:\n'
            i = 1
            for item in load:
                text += str(i) + '. ' + \
                    str(item[1]) + ' - ' + str(item[2]) + '\n'
                i += 1
            await event.answer(text + "\n" + keephelp, keyboard=kbb.get_keyboard())

        if status[0][1] == 'alarms':
            text = event.object.object.message.text
            await event.answer('В какой день вам напомнить?', keyboard=kbdate.get_keyboard())
            alhelplist.update({str(user_id): [text]})
            db.update(db, user_id, 'status', {'screen': 'aldate'})
        if status[0][1] == 'aldate':
            text = event.object.object.message.text
            if text == 'Сегодня':
                data = datetime.now().date()
            elif text == 'Завтра':
                data = datetime.now().date()+timedelta(days=1)
            elif text == 'Послезавтра':
                data = datetime.now().date()+timedelta(days=2)
            else:
                return
            alhelplist[str(user_id)].append(str(data))
            db.update(db, user_id, 'status', {'screen': 'altime'})
            await event.answer('В какое время вам напомнить?', keyboard=kbald.get_keyboard())
        if status[0][1] == 'altime':
            text = event.object.object.message.text
            if text == '09:00':
                db.save(db, user_id, 'alarms', {'text': str(alhelplist[str(
                    user_id)][0]), 'data': str(alhelplist[str(user_id)][1]), 'time': '9'})
            elif text == '12:00':
                db.save(db, user_id, 'alarms', {'text': str(alhelplist[str(
                    user_id)][0]), 'data': str(alhelplist[str(user_id)][1]), 'time': '12'})
            elif text == '15:00':
                db.save(db, user_id, 'alarms', {'text': str(alhelplist[str(
                    user_id)][0]), 'data': str(alhelplist[str(user_id)][1]), 'time': '15'})
            elif text == '18:00':
                db.save(db, user_id, 'alarms', {'text': str(alhelplist[str(
                    user_id)][0]), 'data': str(alhelplist[str(user_id)][1]), 'time': '18'})
            elif text == '21:00':
                db.save(db, user_id, 'alarms', {'text': str(alhelplist[str(
                    user_id)][0]), 'data': str(alhelplist[str(user_id)][1]), 'time': '21'})
            elif text == '23:00':
                db.save(db, user_id, 'alarms', {'text': str(alhelplist[str(
                    user_id)][0]), 'data': str(alhelplist[str(user_id)][1]), 'time': '23'})
            elif text == '03:00':
                db.save(db, user_id, 'alarms', {'text': str(alhelplist[str(
                    user_id)][0]), 'data': str(alhelplist[str(user_id)][1]), 'time': '3'})
            elif text == '06:00':
                db.save(db, user_id, 'alarms', {'text': str(alhelplist[str(
                    user_id)][0]), 'data': str(alhelplist[str(user_id)][1]), 'time': '6'})
            await event.answer("Напоминание сохранено")
            db.update(db, user_id, 'status', {'screen': 'alarms'})
            load = db.load(db, user_id, 'alarms')
            text = 'Ваши напоминания:\n'
            i = 1

            for item in load:
                text += str(i) + '. ' + item[1] + \
                    ' - ' + item[2] + ' в ' + item[3]+':00\n'
                i += 1
            await event.answer(text + '\n' + alarmhelp, keyboard=kbb.get_keyboard())

    user_id = event.object.object.message.peer_id
    print('-команда-главная-'+str(user_id)+'-'+str(datetime.now().time()))
    if len(db.load(db, user_id, 'status')) == 0:
        db.save(db, user_id, 'status', {
                'screen': 'main', 'lastscreen': 'main'})
    db.update(db, user_id, 'status', {'screen': 'main', 'lastscreen': 'main'})
    user_data = (
        await bot.api_context.users.get(user_ids=event.object.object.message.peer_id)
    ).response[0]
    await event.answer(f"Вы можете писать небольшие заметки или поставить напоминания\n \"Сводка\" покажет самое важное на сегодня", keyboard=kbm.get_keyboard())


@bot.message_handler(bot.text_filter(["начать"]))
async def start(event: bot.SimpleBotEvent):
    user_id = event.object.object.message.peer_id
    print('-команда-начать-'+str(user_id)+'-'+str(datetime.now().time()))
    if len(db.load(db, user_id, 'status')) == 0:
        db.save(db, user_id, 'status', {
                'screen': 'main', 'lastscreen': 'main'})
    db.update(db, user_id, 'status', {'screen': 'main', 'lastscreen': 'main'})
    user_data = (
        await bot.api_context.users.get(user_ids=event.object.object.message.peer_id)
    ).response[0]
    await event.answer(f"Здравствуйте, {user_data.first_name}!\nЭто ваш личный бот-ежедневник на каждый день\n\n Здесь вы можете писать небольшие заметки и делать напоминания\n \"Сводка\" покажет самое важное на сегодня", keyboard=kbm.get_keyboard())

bot.run_forever()
