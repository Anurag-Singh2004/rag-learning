import chromadb

client = chromadb.PersistentClient(path="./chroma_storage") #create persistent client (can create in-memory also)

collection = client.get_or_create_collection(name="refund_policy_chunks") #create (or get) a collection

chunks = [
    "Our refund policy applies to all purchases made within 30 days of delivery. However, digital products such as ebooks and",
    "products such as ebooks and software licenses are non-refundable once downloaded. This exception does not apply to subscription plans, which",
    "apply to subscription plans, which can be cancelled anytime for a prorated refund based on unused days. Shipping costs are",
    "unused days. Shipping costs are non-refundable in all cases. To request a refund, contact support with your order number within",
    "with your order number within the eligible window."
] # we are reusing the word-based chunking output from chunking.py

#add chunks to the collection
#ChromaDB needs: documents (the text), and unique ids for each chunk

collection.add(
    documents=chunks,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

query = "Can I get a refund for my subscription?" #search for relevant chunks

results = collection.query(
    query_texts=[query],
    n_results=2  # top 2 most relevant chunks
)

print(results)