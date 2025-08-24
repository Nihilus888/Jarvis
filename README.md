# Jarvis AI
Jarvis AI is a privacy-first, voice-enabled AI assistant you can run locally. Talk to it naturally, just like Jarvis, without sending your data to external AI providers. Personalize it with your own SOPs or train it for specific corporate roles using RAG and ChromaDB.

## Tech Stack
1. Whisper by OpenAI for speech to text
2. Deepseek-llm from Ollama for personal AI model
3. ChromaDB as vector Database for RAG
4. Redis for caching any responses for faster response time
5. Eleven Labs for text to speech
6. Pygames to run the audio file
7. MySQL database for storing logs for training if need be

To allow the system to work, please insert the necessary credentials into the .env file to allow the system to work. You can go to the various websites to get the various API keys to use them. Furthermore, you would need an input device like a speaker and an output device that your system recognises for it to gain input from the user and give output to the user when it is needed. 

## How to run the system
Run deepseek on Ollama:
```
ollama pull deepseek-llm
ollama run deepseek-llm
```

Activate virtual environment:
```
.venv\Scripts\activate
```

Run FastAPI for backend services:
```
uvicorn main:app --reload
```

Call endpoint to get the necessary responses or test the API endpoint
```
curl -X POST http://localhost:8000/generate/audio -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@../tests/Singapore.wav"
```

Run in the background for you to continously talk to Jarvis with the wake words like "Hey Jarvis":
```
app/voice_interface.py
```

RAG and train the AI model for personalisation
```
app/chroma_db.py
```

