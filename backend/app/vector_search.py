import os
from typing import List, Dict, Optional
import numpy as np
from google import generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class VectorSearchService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.enabled = False

        if self.api_key and "your_gemini_api_key" not in self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.enabled = True
                print("Vector Search Service initialized with Gemini Embeddings")
            except Exception as e:
                print(f"WARNING: Failed to initialize embeddings: {e}")
        else:
            print("Vector Search Service in mock mode - no API key")

    def generate_embedding(self, text: str) -> Optional[List[float]]:
        if not self.enabled:
            return self._generate_mock_embedding(text)

        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            print(f"ERROR: Failed to generate embedding: {e}")
            return self._generate_mock_embedding(text)

    def generate_batch_embeddings(self, texts: List[str]) -> List[Optional[List[float]]]:
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        a = np.array(vec1)
        b = np.array(vec2)

        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return float(np.dot(a, b) / (norm_a * norm_b))

    def find_similar(
        self,
        query_embedding: List[float],
        candidate_embeddings: List[List[float]],
        top_k: int = 5
    ) -> List[tuple]:
        similarities = []

        for i, candidate in enumerate(candidate_embeddings):
            if candidate is None:
                continue
            similarity = self.cosine_similarity(query_embedding, candidate)
            similarities.append((i, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def _generate_mock_embedding(self, text: str) -> List[float]:
        np.random.seed(hash(text) % 2**32)
        return np.random.randn(768).tolist()

vector_search_service = VectorSearchService()
