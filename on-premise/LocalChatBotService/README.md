# SduBot
ChatBot created for SDU University
# How to run
Build image after changing
```
git clone https://github.com/baauka/SduBot.git
cd tgbot
docker build -t <image-name:tag> .
```
Or use pre-built image from DockerHub
```
docker pull sultanmukashev/tg-bot:latest
```
Run container using your own OpenAI account API key 
```
docker run sultanmukashev/tg-bot:latest
```
Work with bot in [Telegram](https://t.me/SDUGuideBot).
