def chunk_text(text,chunk_size, overlap):
    """
    text: the full document as a string
    chunk_size: number of words per chunk
    overlap: number of words to repeat between consecutive chunks
    """

    words = text.split()
    chunks =[]

    start=0
    while start<len(words):
        end=start+chunk_size  #end index for this chunk

        chunk=" ".join(words[start:end]) #extract the words for this chunk and join back into a string
        chunks.append(chunk)

        start= start+chunk_size-overlap #move start forward, accounting for overlap
    
    return chunks

# Test with a sample document
sample_text = """Our refund policy applies to all purchases made within 30 days of delivery.
However, digital products such as ebooks and software licenses are non-refundable
once downloaded. This exception does not apply to subscription plans, which can
be cancelled anytime for a prorated refund based on unused days. Shipping costs
are non-refundable in all cases. To request a refund, contact support with your
order number within the eligible window."""


chunks = chunk_text(sample_text, chunk_size=20, overlap=5)

for i, c in enumerate(chunks):
    print(f"--- Chunk {i} ({len(c.split())} words) ---")
    print(c)
    print()
