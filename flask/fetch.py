from flask import Flask, request, jsonify
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

app = Flask(__name__)

# Load investment knowledge base
with open('investment_base.json', 'r') as f:
    knowledge_base = json.load(f)

# Load Sentence Transformer model and create FAISS index
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
texts = [item['recommendation'] for item in knowledge_base]
embeddings = np.array(embedding_model.encode(texts))
dimension = embeddings.shape[1]
faiss_index = faiss.IndexFlatIP(dimension)
faiss_index.add(embeddings)

# Function to retrieve personalized recommendations
def retrieve_recommendation(user_profile, prompt, top_k=2):
    user_profile_text = (
        f"Age: {user_profile.get('age', 'unknown')}, "
        f"Income: {user_profile.get('income', 'unknown')}, "
        f"Employment Status: {user_profile.get('employment_status', 'unknown')}, "
        f"Investment Horizon: {user_profile.get('investment_horizon', 'unknown')}, "
        f"Risk Tolerance: {user_profile.get('risk_tolerance', 'unknown')}, "
        f"Query: {prompt}"
    )
    query_embedding = np.array(embedding_model.encode([user_profile_text]))
    distances, indices = faiss_index.search(query_embedding, top_k)
    relevant_advice = [knowledge_base[idx]['recommendation'] for idx in indices[0]]
    return relevant_advice

@app.route('/get_advice', methods=['POST'])
def get_advice():
    data = request.json
    user_details = data.get('userDetails', {})
    prompt = data.get('prompt', '')

    if not prompt or not user_details:
        return jsonify({'error': 'Invalid input. User details and prompt are required.'}), 400

    # Log query and user details
    print("Received query:")
    print(f"User Details: {user_details}")
    print(f"Prompt: {prompt}")

    advice = retrieve_recommendation(user_details, prompt)
    return jsonify({'advice': advice})

if __name__ == '__main__':
    app.run(port=5000)
