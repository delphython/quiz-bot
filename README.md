# Telegram and VK Quiz Bot

Telegram and VK Quiz Bot is the bot that checks the knowledge of the events of the past years.

## Prerequisites

Python3 should be already installed. Use `pip` to install dependencies:
```bash
pip install -r requirements.txt
```

## Installation for developer mode
You have to set TELEGRAM_TOKEN, VK_TOKEN and Redis connection environment variables before using the script.

1. Create .env file in the project directory.
2. Create the bot and get a token from Telegram, see [this tutorial](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token) for instructions. Copy your Telegram API token to .env file:
```
export TELEGRAM_TOKEN="1234567890:AAHOoGbQZQripXSKTn1ZRmKf6g3-wwwwwww"
```
3. Create the VK group and get a token from VK, see [this tutorial](https://vk.com/dev/access_token?f=2.%20%D0%9A%D0%BB%D1%8E%D1%87%20%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0%20%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D1%81%D1%82%D0%B2%D0%B0) for instructions. Copy your VK API token to .env file:
```
export VK_TOKEN="5f00c1bb11b22d3333a0b444a555d6666d1f7777c2c5e888888888c999e00000e0a3bfa11111b22222a"
```
4. To get Redis connection environment variables (REDIS_HOST, REDIS_PORT, REDIS_PASS and REDIS_DB) you should register [here](https://redis.com/), then choose a Subscription plan and add a new database. Get `REDIS_HOST` and `REDIS_PORT` data in `Public endpoint` section and in `Security` section set `Default user password` - it will be `REDIS_PASS` environment variable. `REDIS_DB` is the name of Redis database as you wish to name. Copy it to .env file:
```
export REDIS_HOST="redis-12345.c12.us-east-1-2.ec2.cloud.redislabs.com"
export REDIS_PORT="12345"
export REDIS_PASS="ruQMaD11FJdbOymGuBgiKk2ZgDP3pAD"
export REDIS_DB="QuestionsAndAnswers"
```


## Usage

For Telegram bot run python script:
```sh
python tg_bot.py
```
For VK bot run python script:
```sh
python vk_bot.py
```
Use Ctrl+C to interrupt the script.   

To save questions and answers to Redis database run python script:
```sh
python save_quiz_to_db.py path_to_file
```
where `path_to_file` - full path to file with questions and answers. You should download quiz files archive from [here](https://dvmn.org/media/modules_dist/quiz-questions.zip)

## Installation for production mode and deploy
For deploying on [Heroku](https://www.heroku.com) you should:
1. Login or register there.
2. Create a new app.
3. Connect GitHub repository.
4. Create `Procfile` in the project root directory and add the text:
```
bot-vk: python3 vk_bot.py
bot-tg: python3 tg_bot.py
```
5. Add TELEGRAM_TOKEN, VK_TOKEN, REDIS_HOST, REDIS_PORT, REDIS_PASS and REDIS_DB environment variables in the Settings tab of the Heroku site.
6. Don't forget to renew the project repository on Heroku.

## Try the bots
1. Link to the Telegram bot: [@my_cooking_timer_bot](https://t.me/my_cooking_timer_bot)
![alt text](./telegram-bot.gif)

2. Link to the VK bot: [Test Group](https://vk.com/im?sel=-210593620)
![alt text](./vk-bot.gif)

## Meta

Vitaly Klyukin — [@delphython](https://t.me/delphython) — [delphython@gmail.com](mailto:delphython@gmail.com)

[https://github.com/delphython](https://github.com/delphython/)
