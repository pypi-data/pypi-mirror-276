# text_eval/text_similarity.py

import logging
from typing import List
from sentence_transformers import SentenceTransformer, util
import torch

logger = logging.getLogger(__name__)

class TextSimilarityJudge:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        
    def judge(self, texts1: List[str], texts2: List[str], batch_size: int = 32, num_workers: int = 0) -> List[float]:
        assert len(texts1) == len(texts2), "texts1 and texts2 lists must have equal length"
        embeddings1 = self.model.encode(texts1, convert_to_tensor=True, batch_size=batch_size, num_workers=num_workers)
        embeddings2 = self.model.encode(texts2, convert_to_tensor=True, batch_size=batch_size, num_workers=num_workers)
        similarities = util.pytorch_cos_sim(embeddings1, embeddings2)
        return [float(similarity) for similarity in similarities.diagonal()]

class TextSimilarity:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.similarity_judge = TextSimilarityJudge(model_name)
        
    def compute_score(self, texts1: List[str], texts2: List[str]) -> List[float]:
        try:
            scores = self.similarity_judge.judge(texts1, texts2)
        except Exception as e:
            logger.error(f"Error computing text similarity score: {e}")
            scores = [0.0] * len(texts1)
        return scores
    
    def compute_pairwise_score(self, ground_truths: List[str], answers: List[str]) -> List[List[float]]:
        try:
            embeddings1 = self.similarity_judge.model.encode(ground_truths, convert_to_tensor=True)
            embeddings2 = self.similarity_judge.model.encode(answers, convert_to_tensor=True)
            similarities = util.pytorch_cos_sim(embeddings1, embeddings2)
            return similarities.tolist()
        except Exception as e:
            logger.error(f"Error computing pairwise text similarity score: {e}")
            return []

if __name__ == "__main__":
    texts1 = ["This is a sample sentence.", "Machine learning is fascinating."]
    texts2 = ["This is another example sentence.", "Artificial intelligence and machine learning are fascinating fields."]
    
    similarity_model = TextSimilarity()
    similarity_scores = similarity_model.compute_score(texts1, texts2)
    pairwise_scores = similarity_model.compute_pairwise_score(texts1, texts2)
    
    print(f"Similarity Scores: {similarity_scores}")
    print(f"Pairwise Similarity Scores: {pairwise_scores}")
