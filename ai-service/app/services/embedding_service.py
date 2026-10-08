import numpy as np
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.config import settings
from openai import OpenAI

class EmbeddingService:
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_openai_api_key_here":
            try:
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            except Exception:
                self.client = None

    def get_embedding(self, text: str) -> List[float]:
        """Fetch OpenAI embedding vector if client is available."""
        if self.client:
            try:
                response = self.client.embeddings.create(
                    input=text[:8000],
                    model=settings.EMBEDDING_MODEL
                )
                return response.data[0].embedding
            except Exception:
                pass
        return []

    def compute_similarity(self, text1: str, text2: str) -> float:
        """Compute semantic cosine similarity between two texts."""
        if not text1 or not text2:
            return 0.0

        # Try OpenAI embeddings if available
        if self.client:
            try:
                emb1 = self.get_embedding(text1)
                emb2 = self.get_embedding(text2)
                if emb1 and emb2:
                    v1 = np.array(emb1)
                    v2 = np.array(emb2)
                    sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
                    return float(np.clip(sim, 0.0, 1.0))
            except Exception:
                pass

        # Fallback to local TF-IDF N-gram cosine similarity
        try:
            vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            # Normalization scale for keyword/phrasing overlap
            return float(np.clip(sim * 1.5, 0.0, 1.0))
        except Exception:
            # Fallback exact word overlap
            s1 = set(text1.lower().split())
            s2 = set(text2.lower().split())
            if not s1 or not s2:
                return 0.0
            return float(len(s1.intersection(s2)) / max(len(s1), len(s2)))

embedding_service = EmbeddingService()
