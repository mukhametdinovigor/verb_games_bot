# Чат боты для Telegram и VK

Это чатботы для службы поддержки, использующий сервис распознавания естественного языка от Google 
[DialogFlow](https://dialogflow.cloud.google.com/).

Бот распознает сообщения пользователей и отвечает соответствующим текстом.  

Пообщаться с ботом можно:

- в Телеграм [@VerbGamesBot](https://t.me/VerbGamesBot)
- Вконтакте в группе [Verb_Games](https://vk.com/club208071622) кликнуть на `Написать сообщение`

Также пример работы ботов можно посмотреть на гифке

- Бот для Telegram

![бот для Telegram](examples/demo_tg_bot.gif)

- Бот для VK

![бот для VK](examples/demo_vk_bot.gif)



## Как запустить

Скачайте код:
```sh
git clone https://github.com/mukhametdinovigor/verb_games_bot.git
```

Перейдите в каталог проекта:
```sh
cd verb_games_bot
```

[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:
- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

У вас должен быть [зарегистрированный бот в Telegram](https://telegram.me/BotFather)

У вас должен быть [аккаунт в DialogFlow](https://dialogflow.cloud.google.com/) и проект в нём.
В проекте вам нужно создать новый Intent, добавить Training phrases и добавить Response.
Чтобы обучить DialogFlow автоматически, запустите в командной строке:

```sh
python teach_dialogflow.py
```
для этого у вас в корне проекта должен быть файл с вопросами и ответами`questions.json`, со следующей структурой:

```json
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
```

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` в корне проекта
и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны переменные:
- `BOT_TOKEN` — токен рабочего бота в телеграм.
- `VK_TOKEN` — токен Вконтакте
- `GC_PROJECT_ID` — идентификатор проекта [Google Cloud](https://cloud.google.com/dialogflow/es/docs/quick/setup)
- `GOOGLE_APPLICATION_CREDENTIALS` - путь к json файлу с учетными данными от [Google](https://cloud.google.com/docs/authentication/getting-started)
- `BUG_REPORTING_BOT_TOKEN` - токен бота в телеграм, куда будут отправлятся сообщения об ошибках
- `CHAT_ID` - ваш chat_id в телеграм

Запустите ботов:

- Телеграм

```sh
python tg_bot.py
```

- Вконтакте

```sh
python vk_bot.py
```


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
