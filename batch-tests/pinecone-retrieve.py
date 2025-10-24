from pinecone.grpc import PineconeGRPC as Pinecone
from dotenv import load_dotenv
import os
import sys

# -----------------------------
# Step 0: Load environment variables
# -----------------------------
load_dotenv()

# Get Pinecone API key from .env file
api_key = os.getenv("PINECONE_API_KEY")

if not api_key:
    print("❌ Missing PINECONE_API_KEY in .env file")
    sys.exit(1)

# -----------------------------
# Step 1: Initialize Pinecone client
# -----------------------------
try:
    pc = Pinecone(api_key=api_key)
    print("✅ Pinecone client initialized successfully")
except Exception as e:
    print("❌ Failed to initialize Pinecone client:", e)
    sys.exit(1)

# -----------------------------
# Step 2: Connect to your index
# -----------------------------
index_host = "quickstart-py-02vwk3u.svc.aped-4627-b74a.pinecone.io"  # Replace with your index host

try:
    index = pc.Index(host=index_host)
    print(f"✅ Connected to index at host: {index_host}")
except Exception as e:
    print("❌ Failed to connect to index:", e)
    sys.exit(1)

# -----------------------------
# Step 3: Fetch specific vectors from namespace
# -----------------------------
vector_ids = ["document1#first", "document1#second"]  # Add more IDs as needed

try:
    all_vectors = index.fetch(ids=vector_ids, namespace="example-namespace")
    print(f"✅ Successfully fetched {len(all_vectors.vectors)} vectors\n")
except Exception as e:
    print("❌ Failed to fetch vectors:", e)
    sys.exit(1)

# -----------------------------
# Step 4: Print each vector and metadata
# -----------------------------
if not all_vectors.vectors:
    print("⚠️ No vectors found for the given IDs.")
else:
    for vid, vec in all_vectors.vectors.items():
        print("🆔 ID:", vid)
        print("📏 Vector Dimension:", len(vec.values))
        print("🔢 First 10 Vector Values:", vec.values[:10], "...")
        print("🧾 Metadata:", vec.metadata)
        print("=" * 60)
