import os
from openai import OpenAI
from pinecone import Pinecone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Connect to Pinecone index
index_name = "hubspot-llms"
index = pc.Index(index_name)

# User input
query = input("Ask a question about HubSpot accounts: ")

# Step 1: Embed the user query
embedding = client.embeddings.create(
    input=query,
    model="text-embedding-3-small"
).data[0].embedding

# Step 2: Search Pinecone
search_results = index.query(
    vector=embedding,
    top_k=5,
    include_metadata=True
)

# Step 3: Extract and display top chunks
matches = search_results.get("matches", [])
if not matches:
    print("No relevant chunks found.")
    exit()

print("\n🔍 Top Matches:")
for i, match in enumerate(matches):
    print(f"\nChunk {i+1}:\n{match['metadata']['text']}")

# Step 4 (Optional): Use GPT to generate an answer
use_gpt = input("\n🧠 Use GPT-4 to summarize answer from chunks? (y/n): ").lower()
if use_gpt == "y":
    context = "\n\n".join([m["metadata"]["text"] for m in matches])
    prompt = f"Use the following context to answer the question:\n\n{context}\n\nQ: {query}\nA:"
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers based only on provided HubSpot documentation."},
            {"role": "user", "content": prompt}
        ]
    )
    
    answer = response.choices[0].message.content
    print(f"\n✅ Answer:\n{answer}")
