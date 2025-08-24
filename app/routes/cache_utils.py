import redis
import json
from rapidfuzz import fuzz

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

CACHE_THRESHOLD = 85  # Adjust as needed

# --- Fuzzy Match Cache ---
def get_cached_response_fuzzy(prompt, threshold=CACHE_THRESHOLD):
    all_keys = redis_client.keys("response:*")
    for key in all_keys:
        cached_prompt = key.replace("response:", "")
        similarity = fuzz.ratio(prompt, cached_prompt)
        if similarity >= threshold:
            return redis_client.get(key)
    return None

# --- Exact Match Cache ---
def get_cached_response_exact(prompt: str):
    return redis_client.get(f"response:{prompt}")

# --- Embedding Cache ---
def get_embedding_from_cache(text: str):
    emb_json = redis_client.get(f"embedding:{text}")
    if emb_json:
        return json.loads(emb_json)
    return None

def cache_embedding(text: str, embedding):
    redis_client.set(f"embedding:{text}", json.dumps(embedding))

def cached_local_embedder(texts, model):
    embeddings = []
    for text in texts:
        emb = get_embedding_from_cache(text)
        if emb is None:
            emb = model.encode([text], convert_to_numpy=True)[0].tolist()
            cache_embedding(text, emb)
        embeddings.append(emb)
    return embeddings

# --- Chatbot Response Cache ---
def get_response_cache(prompt: str):
    return redis_client.get(f"response:{prompt}")

def cache_response(prompt: str, response: str):
    redis_client.set(f"response:{prompt}", response)

def clear_cache():
    for key in redis_client.keys("response:*"):
        redis_client.delete(key)
    for key in redis_client.keys("embedding:*"):
        redis_client.delete(key)

clear_cache()