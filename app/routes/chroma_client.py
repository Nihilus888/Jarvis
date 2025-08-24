from sentence_transformers import SentenceTransformer
import chromadb

try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Error loading sentence-transformers model: {e}")

def local_embedder(texts):
    try:
        embeddings = model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
    except Exception as e:
        print(f"Error in local_embedder: {e}")
        return []

try:
    client = chromadb.Client()
    collection = client.create_collection(name="jarvis_sops")  # ✅ Changed name
    collection.set_embedding_function(local_embedder)

    # DELETE all existing entries before adding new ones
    collection.delete()
except Exception as e:
    print(f"Error initializing Chroma client or collection: {e}")

# Example SOP documents for Jarvis
documents = [
    "If Jarvis cannot recognize a wake word, ensure the microphone is connected properly.",
    "If Jarvis's speech output is distorted, try restarting the TTS engine.",
    "If Jarvis is not responding to commands, check the API connection status."
]

ids = [f"doc{i+1}" for i in range(len(documents))]

try:
    collection.add(documents=documents, ids=ids)
except Exception as e:
    print(f"Error adding documents to collection: {e}")

def query_chroma(query_text, top_k=2):
    try:
        results = collection.query(query_texts=[query_text], n_results=top_k)
        return results['documents'][0] if results['documents'] else []
    except Exception as e:
        print(f"Error querying Chroma: {e}")
        return []

if __name__ == "__main__":
    queries = [
        "Jarvis is not hearing me",
        "Jarvis voice sounds weird",
        "Jarvis is not following commands",
    ]

    for q in queries:
        res = query_chroma(q, top_k=2)
        print(f"Query: {q}\nResults: {res}\n")
