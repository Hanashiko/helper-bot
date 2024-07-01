from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import config as cfg
from datetime import datetime
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=cfg.TOKEN_BOT)
dp = Dispatcher(bot,storage=MemoryStorage())
storage = MemoryStorage()

# FSM
class FSMQuestion(StatesGroup):
    quest = State()
class FSMSuggestion(StatesGroup):
    suggest = State()

# keyboards
b1 = KeyboardButton('Запитання')
b2 = KeyboardButton('Пропозиція')
kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.add(b1).add(b2)

# startup
async def on_startup(_):
  me = await bot.get_me()
  UserInfo = await bot.get_chat_member(me.id, me.id)
  username = f"@{UserInfo.user.username}"
  print(f"Бота запущено ({username} - {me.first_name})")
  await bot.send_message(cfg.OWNER_ID, f"Запуск бота відбувся успішно\n{datetime.today()}")

# handlers
@dp.message_handler(commands=['start'])
async def cmd_start(mes: types.Message):
    await mes.reply("Вітаю. Я бот створений Hanashi для проєкту UA Manga. В мені ви можете запитати що вас цікавить, чи запропонувати якусь ідея для покращення. Перелік моїх можливостей ви можете перглянути використовуючи команду /help. Також можите натискати кнопки внизу для відповідних задач.",reply_markup=kb_start)
    if mes.from_user.id == cfg.CHECKER_ID:
        await mes.reply("Щоб відповісти людині використовуйте таку конструкцію: /send id message. Приклад: /send 5697846986 Мені сподобалась твоя пропозиція, роскажи детальніше щодо останього пункту.")

@dp.message_handler(commands=['help']) 
async def cmd_help(mes: types.Message):
   await mes.reply("Ось мої можливості, та команди:\n· /question [питання] - запитати щось(командовий аналог кнопки).\nПриклад використання: /question навіщо потрібен ваш проєкт?\n· /suggestion [пропозиція] - запропонувати щось(командовий аналог кнопки).\nПриклад використання: /suggestion зробити гугл форму з цікавими(не перекладеними) проєктами.\n· /bot [питання] - надати якесь питання, пропозицію, чи поправку щодо бота.\nПриклад використання: /bot виправте баг з відповідю.")
   if mes.from_user.id == cfg.CHECKER_ID:
      await mes.reply("Команди для адміністратора:\n· /send [id] [message] - написати щось користувачу.\nПриклад використання: /send 5697846986 ми реалізували вашу ідею")

@dp.message_handler(commands=['send'])
async def cmd_send(mes: types.Message): 
  if mes.from_user.id != cfg.CHECKER_ID or mes.from_user.id != cfg.OWNER_ID:
    await mes.reply("У вас недостатньо прав для цієї дії")
  else:
    args = mes.text.split()
    if args == ['/send']:
      await mes.reply("Ось формат написання цієї команди: /send id повідомлення")
    else:
      if not args[1]:
        await mes.reply("Ви не вказали id людини, можливо поставили зайвий пробіл.\nОсь формат написання цієї команди: /send id повідомлення")
      else:
        try:
          arg1 = args[1]
          arg2 = " ".join(args[2:])
        except:
          await mes.reply("Виникла якась помилка з виявленям аргументів.\nОсь формат написання цієї команди: /send id повідомлення")
          return
        try:
          await bot.send_message(arg1, f"Відповідь адміністратора:\n{arg2}")
        except:
          await mes.reply("Я не зміг написати користувачу.\nМожливі причини цього:\n· Ви помились в написанні id(приклад, як повино виглядати id користувача: 5697846986).\n· Я не маю діалогу з цим користувачем.\n· Цей користувач заблокував мене.")
          return
        UserInfo = await bot.get_chat_member(arg1, arg1)
        username = f"@{UserInfo.user.username}"
        await mes.reply(f"Я написав `{arg1}`({username}):\n{arg2}", parse_mode='markdown')

@dp.message_handler(commands=['question'])
async def cmd_question(mes: types.Message):
  args = mes.text.split()
  if args == ['/question']:
    await mes.reply("Ви забули вказати питання.\nФормат написання команди: /question питання")
  else:
    try:
      UserInfo = await bot.get_chat_member(mes.from_user.id, mes.from_user.id)
      username = f"@{UserInfo.user.username}"
    except:
      mes.reply("У мене виникли труднощі з вашою командою. Будь ласка напишіть розробнику бота(команда /bot), щоб ми змогли покращити нашого бота")
      return
    quest = " ".join(args)
    bot.send_message(cfg.CHECKER_ID, f"Користувач {username} (`{mes.from_user.id}`), написав питання:\n{quest}", parse_mode='markdown')
    mes.reply("Я успішно надіслав ваше запитання адміністратору.")

@dp.message_handler(commands=['suggestion'])
async def cmd_question(mes: types.Message):
  args = mes.text.split()
  if args == ['/suggestion']:
    await mes.reply("Ви забули вказати пропозицію.\nФормат написання команди: /suggestion пропозиція")
  else:
    try:
      UserInfo = await bot.get_chat_member(mes.from_user.id, mes.from_user.id)
      username = f"@{UserInfo.user.username}"
    except:
      mes.reply("У мене виникли труднощі з вашою командою. Будь ласка напишіть розробнику бота(команда /bot), щоб ми змогли покращити нашого бота")
      return
    sugge = " ".join(args)
    bot.send_message(cfg.CHECKER_ID, f"Користувач {username} (`{mes.from_user.id}`), написав пропозицію:\n{sugge}", parse_mode='markdown')
    mes.reply("Я успішно надіслав вашу пропозицію адміністратору.")

@dp.message_handler(commands=['bot'])
async def cmd_question(mes: types.Message):
  args = mes.text.split()
  if args == ['/bot']:
    await mes.reply("Ви забули вказати текст після команди.\nФормат написання команди: /bot повідомлення щодо бота")
  else:
    try:
      UserInfo = await bot.get_chat_member(mes.from_user.id, mes.from_user.id)
      username = f"@{UserInfo.user.username}"
    except:
      mes.reply("У мене виникли труднощі з вашою командою. Будь ласка напишіть розробнику бота(@hanashiko), щоб ми змогли покращити нашого бота")
      return
    abot = " ".join(args)
    bot.send_message(cfg.OWNER_ID, f"Користувач {username} (`{mes.from_user.id}`), написав поправку щодо бота:\n{abot}", parse_mode='markdown')
    mes.reply("Я успішно надіслав вашу пропозицію творцю бота.")

# FSM commands
# FSM Question
@dp.message_handler(lambda message: message.text and 'запитання' in message.text.lower(), state=None)
async def cmd_quest(mes: types.Message):
  await mes.reply("Напишіть ваше запитання:\n(щоб відмінити команду напишіть /cancel)")
  await FSMQuestion.quest.set()

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMQuestion):
	current_state = await state.get_state()
	if current_state is None:
		return
	await state.finish()
	await message.reply("Я відмінив вашу дію.")
                
@dp.message_handler(state=FSMQuestion.quest)
async def load_name(mes: types.Message, state: FSMQuestion):
  async with state.proxy() as data:
    data['quest'] = mes.text
  try:
    UserInfo = await bot.get_chat_member(mes.from_user.id, mes.from_user.id)
    username = f"@{UserInfo.user.username}"
  except:
    mes.reply("У мене виникли труднощі з вашою командою. Будь ласка напишіть розробнику бота(команда /bot), щоб ми змогли покращити нашого бота")
    return
  try:
    await bot.send_message(cfg.CHECKER_ID, f"Користувач {username} (`{mes.from_user.id}`) запитав:\n{mes.text}",parse_mode='markdown')
    await bot.send_message(cfg.CHECKER_ID, f"Щоб відповісти використовуйте команду /send. Формат використання: /send id повідомлення")
  except:
      mes.reply("У мене виникли труднощі з вашою командою. Будь ласка напишіть розробнику бота(команда /bot), щоб ми змогли покращити нашого бота")
      await state.finish()
      return
  await mes.reply("Я відправив адміністратору ваше запитання.")
  await state.finish()

# FSM Suggestion
@dp.message_handler(lambda message: message.text and 'пропозиція' in message.text.lower(), state=None)
async def cmd_suggest(mes: types.Message):
  await mes.reply("Напишіть вашу пропозицію:\n(щоб відмінити команду напишіть /cancel)")
  await FSMSuggestion.suggest.set()

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMSuggestion):
	current_state = await state.get_state()
	if current_state is None:
		return
	await state.finish()
	await message.reply("Я відмінив вашу дію.")   

@dp.message_handler(state=FSMSuggestion.suggest)
async def load_name(mes: types.Message, state: FSMSuggestion):
  async with state.proxy() as data:
    data['suggest'] = mes.text
  try:
    UserInfo = await bot.get_chat_member(mes.from_user.id, mes.from_user.id)
    username = f"@{UserInfo.user.username}"
  except:
    mes.reply("У мене виникли труднощі з вашою командою. Будь ласка напишіть розробнику бота(команда /bot), щоб ми змогли покращити нашого бота")
    return
  try:
    await bot.send_message(cfg.CHECKER_ID, f"Користувач {username} (`{mes.from_user.id}`) запропонував:\n{mes.text}",parse_mode='markdown')
    await bot.send_message(cfg.CHECKER_ID, f"Щоб відповісти використовуйте команду /send. Формат використання: /send id повідомлення")
  except:
      mes.reply("У мене виникли труднощі з вашою командою. Будь ласка напишіть розробнику бота(команда /bot), щоб ми змогли покращити нашого бота")
      await state.finish()
      return
  await mes.reply("Я відправив адміністратору вашу пропозицію.")
  await state.finish()

 executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
