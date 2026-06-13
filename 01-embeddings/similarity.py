from sentence_transformers import SentenceTransformer
import numpy as np

def cosine_similarity(A, B):
    dot_product = np.dot(A, B)
    magnitude_A = np.sqrt(np.sum(A * A))
    magnitude_B = np.sqrt(np.sum(B * B))
    return dot_product / (magnitude_A * magnitude_B)


# Load a small, fast embedding model (good for learning, ~80MB)
model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
    "How do I reset my password?",
    "Steps to recover account access",
    "Best pizza recipe with extra cheese"
]

#convert sentences to embeddings
embeddings= model.encode(sentences)  #numpy ndarray

#check the shape- how many dimensions per sentence
print("Shape:",embeddings.shape)

#compute similarity between sentence 0 and 1 (related meaning)
sim_0_1 = cosine_similarity(embeddings[0], embeddings[1])

#compute similarity between sentence 0 and 2 (unrelated)
sim_0_2 = cosine_similarity(embeddings[0],embeddings[2])

print("Password vs Recover Access:", sim_0_1)
print("Password vs Pizza:", sim_0_2)