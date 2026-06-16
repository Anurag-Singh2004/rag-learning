import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="./chroma_storage_v2")
collection = client.get_or_create_collection(
    name="refund_policy_explicit",
    metadata={"hnsw:space": "cosine"}
)

def retrieve_with_threshold(query, collection, model, k=5, threshold=0.5):
    """
    Returns only chunks below the distance threshold (i.e. similar enough).
    If NONE qualify, returns an empty list (signal: 'no relevant context found').
    """
    query_embedding = model.encode(query).tolist()

    results= collection.query(
        query_embeddings=[query_embedding],
        n_results = k
    )
    documents=results['documents'][0]
    distances=results['distances'][0]

    filtered = []
    for doc, dist in zip(documents, distances):
        if(dist<threshold):
            filtered.append((doc,dist))
        
    return filtered

test_queries = [
    "Can I get a refund for my subscription?",
    "What's the weather like today?"  # completely irrelevant to our docs
]

for q in test_queries:
    print(f"\nQuery: {q}")
    results = retrieve_with_threshold(q,collection,model, k=2, threshold=0.5)
    if not results:
        print("  → No relevant context found.")
    else:
        for doc,dist in results:
            print(f"  → (distance={dist:.3f}) {doc}")