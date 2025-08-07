.venv\Scripts\activate

uvicorn main:app --reload

curl -X POST http://localhost:8000/generate/audio -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@../tests/Singapore.wav"
