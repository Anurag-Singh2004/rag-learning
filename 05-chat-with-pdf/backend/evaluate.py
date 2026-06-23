import os
from rag_pipeline import ingest_pdf, retrieve_with_threshold, rerank

# self-contained: ingest the test PDF within THIS process
PDF_PATH = os.path.join(os.path.dirname(__file__), "orbitnote_policy.pdf")

with open(PDF_PATH, "rb") as f:
    file_bytes = f.read()

print("Ingesting test document...")
chunks_created = ingest_pdf(file_bytes, "orbitnote_policy.pdf")
print(f"Ingested {chunks_created} chunks\n")

test_cases = [
    {"question": "How much does the Pro plan cost?", "expected_keyword": "$9"},
    {"question": "Can I get a refund on a monthly subscription?", "expected_keyword": "not eligible for refunds"},
    {"question": "How long until inactive free accounts get deleted?", "expected_keyword": "18 months"},
    {"question": "What happens if I edit the same note offline on two devices?", "expected_keyword": "conflict"},
    {"question": "Is two-factor authentication required on the Team plan?", "expected_keyword": "mandatory"},
    {"question": "What's the API rate limit for Pro accounts?", "expected_keyword": "1,000"},
    {"question": "How long can I download my data after cancelling?", "expected_keyword": "90 days"},
]


def check_hit(chunks, keyword):
    keyword_lower = keyword.lower()
    for chunk in chunks:
        if keyword_lower in chunk["text"].lower():
            return True
    return False


def evaluate():
    vector_hits = 0
    reranked_hits = 0

    for case in test_cases:
        question = case["question"]
        keyword = case["expected_keyword"]

        candidates = retrieve_with_threshold(question, k=10, threshold=0.6)
        reranked = rerank(question, candidates, top_n=3)

        vector_hit = check_hit(candidates, keyword)
        reranked_hit = check_hit(reranked, keyword)

        vector_hits += vector_hit
        reranked_hits += reranked_hit

        status = "✓" if reranked_hit else "✗"
        print(f"{status} Q: {question}")
        print(f"  keyword='{keyword}' | vector={vector_hit} | reranked={reranked_hit}")
        if not reranked_hit and candidates:
            print(f"  best candidate: {candidates[0]['text'][:100]}")
        print()

    total = len(test_cases)
    print(f"Vector search hit rate:  {vector_hits}/{total} = {vector_hits/total:.0%}")
    print(f"Re-ranked hit rate:      {reranked_hits}/{total} = {reranked_hits/total:.0%}")


if __name__ == "__main__":
    evaluate()