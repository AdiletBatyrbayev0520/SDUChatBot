# SduBot
ChatBot created for SDU University
# How to run
Build image after changing
```
git clone <this repo url>
cd SduBot
docker build -t <image-name:tag> .
```
Or use pre-built image from DockerHub
```
docker pull sultanmukashev/sdu-bot
```
Run container using your own OpenAI account API key 
```
docker run -it --rm -e OPENAI_API_KEY=<твой апи ключ от гпт> sultanmukashev/sdu-bot:latest
```
Work with model in command promt.
