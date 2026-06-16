import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="./chroma_storage_v2")

collection = client.get_or_create_collection(
    name = "refund_policy_explicit",
    metadata= {"hnsw:space":"cosine"} #explicitly set distance metric to cosine
)

chunks = [
    "Our refund policy applies to all purchases made within 30 days of delivery.",
    "Digital products such as ebooks and software licenses are non-refundable once downloaded.",
    "Subscription plans can be cancelled anytime for a prorated refund based on unused days.",
    "Shipping costs are non-refundable in all cases.",
    "To request a refund, contact support with your order number within the eligible window."
]

chunk_embeddings= model.encode(chunks) #generate embeddings ourselves

# add embeddings to collection
collection.add(
    documents=chunks,
    embeddings=chunk_embeddings,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

query = "Can I get a refund for my subscription?"

query_embedding = model.encode(query)

results = collection.query(
    query_embeddings= query_embedding,
    n_results=2
)

print(results)
