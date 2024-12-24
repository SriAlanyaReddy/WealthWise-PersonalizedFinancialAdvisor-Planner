import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# Load the investment base from the JSON file
with open('investment_base.json', 'r') as f:
    knowledge_base = json.load(f)

# Load the Sentence Transformer model for embeddings
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Extract the recommendations from the knowledge base
texts = [item['recommendation'] for item in knowledge_base]

# Generate embeddings for each recommendation
embeddings = np.array(embedding_model.encode(texts))

# Build FAISS Index (using Cosine Similarity via Inner Product)
dimension = embeddings.shape[1]  # Should be 384 for the "all-MiniLM-L6-v2" model
faiss_index = faiss.IndexFlatIP(dimension)
faiss_index.add(embeddings)

# Function to retrieve personalized recommendations based on user profile
def retrieve_recommendation(user_profile, top_k=2):
    # Combine user profile into a single text query
    user_profile_text = (
        f"Age: {user_profile['age']}, Income: {user_profile['income']}, "
        f"Employment Status: {user_profile['employment_status']}, Investment Horizon: {user_profile['investment_horizon']}, "
        f"Risk Tolerance: {user_profile['risk_tolerance']}"
    )

    # Create an embedding for the user profile query
    query_embedding = np.array(embedding_model.encode([user_profile_text]))

    # Search the FAISS index for the most similar advice
    distances, indices = faiss_index.search(query_embedding, top_k)

    # Retrieve the corresponding recommendations from the knowledge base
    relevant_advice = [knowledge_base[idx]['recommendation'] for idx in indices[0]]

    # Print recommendations to the console (for debugging/verification)
    print("Retrieved Recommendations:")
    for advice in relevant_advice:
        print(advice)

    return relevant_advice

