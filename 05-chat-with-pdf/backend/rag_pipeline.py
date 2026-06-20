from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import io
import os
from groq import Groq
from google import genai
from dotenv import load_dotenv
from sentence_transformers import CrossEncoder

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path=os.path.join(os.path.dirname(__file__), "chroma_storage"))
collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)

def extract_text_from_pdf(file_bytes):
    """Extract all text from a PDF file's raw bytes."""

    reader = PdfReader(io.BytesIO(file_bytes))  #bytesio : standard library tool that wraps raw bytes and makes them BEHAVE like a file

    text=""
    #reader.pages gives you a list of page objects. Each page object has a method .extract_text() that pulls the readable text out of that page
    for page in reader.pages:
        text+= page.extract_text()
    
    return text

def chunk_text(text, chunk_Size=100,overlap=20):
    words = text.split()
    chunks=[]
    start=0
    while start < len(words):
        end=start+chunk_Size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = start+chunk_Size-overlap
    
    return chunks

# todo: if same filename uploaded twice with different content,
# old chunks may not fully get replaced (could leave stale leftover
# chunks if new file has fewer chunks than old one). 
# Fix: delete existing chunks for this filename before adding new ones.
#but this fix is very simple, later we can change the architecture and  generate IDs that are GUARANTEED unique regardless of filename collisions, e.g., using a UUID or content hash, decoupling "uniqueness" from "filename" entirely. 

def ingest_pdf(file_bytes, filename):
    """Full pipeline: PDF bytes -> text -> chunks -> embeddings -> stored in ChromaDB."""

    existing = collection.get(where={"source": filename})
    if existing['ids']:
        collection.delete(ids=existing['ids'])  # clear old chunks for this filename first

    text = extract_text_from_pdf(file_bytes)
    chunks = chunk_text(text)
    embeddings = model.encode(chunks)
    ids = [f"{filename}_{i}" for i in range(len(chunks))]

    collection.add(
        documents= chunks,
        embeddings= embeddings.tolist(),
        ids=ids,
        metadatas=[{"source": filename} for _ in chunks] ## track which file each chunk came from
    )

    return len(chunks)

def retrieve_with_threshold(query, k=5, threshold=0.5):
    """Stage 1: Embed query, search ChromaDB, filter by distance threshold."""

    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings= [query_embedding],
        n_results=k
    )
    documents = results['documents'][0]
    distances = results['distances'][0]
    metadatas = results['metadatas'][0]

    filtered = []
    for doc, dist, meta in zip(documents, distances, metadatas):
        if dist < threshold:
            filtered.append({"text": doc, "source": meta['source']})
    
    return filtered

def rerank(query, candidates, top_n=3):
    """Stage 2: expensive, precise re-scoring on the shortlist."""

    if not candidates:
        return []
    
    # Step 1: cross-encoder needs [query, chunk] pairs
    pairs = [[query, c["text"]] for c in candidates]

    # Step 2: get relevance scores for each pair
    scores= reranker.predict(pairs)

    # Step 3: sort chunks by score, descending (higher = more relevant for cross-encoders)
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)

    # Step 4: return just the top_n chunk texts
    return [chunk for chunk, score in ranked[:top_n]]

def build_prompt(question, context_chunks):
    """Construct the final prompt sent to the LLM."""

    if not context_chunks:
        context = "No relevant context was found in the document."
    else:
        context = "\n\n".join(c["text"] for c in context_chunks)
    
    prompt = f"""Answer the question using ONLY the context below. If the context doesn't contain enough information to answer, say so explicitly — do not make up information.

Context:
{context}

Question: {question}

Answer:"""
    return prompt

def generate_answer(question, provider="groq"):

    """Full RAG generation: retrieve, build prompt, call LLM."""

    candidates = retrieve_with_threshold(question, k=10, threshold=0.5)
    chunks = rerank(question, candidates, top_n=3)
    prompt = build_prompt(question, chunks)

    if provider == "groq":
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content

    elif provider == "gemini":
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        answer = response.text
    
    else:
        raise ValueError("Unknown provider")
    
    return answer, len(chunks), chunks

def list_documents():
    all_data = collection.get()
    sources = {}
    for meta in all_data['metadatas']:
        source = meta['source']
        sources[source] = sources.get(source, 0) + 1
    return [{"filename": k, "chunks": v} for k, v in sources.items()]