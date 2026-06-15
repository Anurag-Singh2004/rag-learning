from sentence_transformers import SentenceTransformer

def chunk_text_by_tokens(text,tokenizer,max_tokens,overlap_tokens):
    """
    text: full document string
    tokenizer: the model's tokenizer
    max_tokens: max tokens per chunk
    overlap_tokens: tokens to overlap between chunks
    """
    tokens= tokenizer.tokenize(text)

    chunks=[]
    start=0
    while start<len(tokens):
        end= start+max_tokens
        chunk_tokens=tokens[start:end]

        chunk_text = tokenizer.convert_tokens_to_string(chunk_tokens) #convert tokens back into a readable string
        chunks.append(chunk_text)

        start= start+max_tokens-overlap_tokens
    
    return chunks

model = SentenceTransformer('all-MiniLM-L6-v2')
tokenizer = model.tokenizer

sample_text = """Our refund policy applies to all purchases made within 30 days of delivery.
However, digital products such as ebooks and software licenses are non-refundable
once downloaded. This exception does not apply to subscription plans, which can
be cancelled anytime for a prorated refund based on unused days. Shipping costs
are non-refundable in all cases. To request a refund, contact support with your
order number within the eligible window."""

chunks= chunk_text_by_tokens(sample_text, tokenizer, max_tokens=20, overlap_tokens=5)

for i, c in enumerate(chunks):
    chunk_token_count = len(tokenizer.tokenize(c))
    print(f"--- Chunk {i} ({chunk_token_count} tokens) ---")
    print(c)
    print()