import os
import json
import hashlib
import math
import logging
from langchain_google_genai import GoogleGenerativeAIEmbeddings

logger = logging.getLogger(__name__)

class RunbookVectorStore:
    def __init__(self, runbooks_dir=None, cache_path=None):
        possible_paths = ["/app/runbooks", "./runbooks", "../runbooks", "./backend/runbooks"]
        self.runbooks_dir = None
        if runbooks_dir:
            if os.path.exists(runbooks_dir) and os.path.isdir(runbooks_dir):
                self.runbooks_dir = runbooks_dir
        else:
            for path in possible_paths:
                if os.path.exists(path) and os.path.isdir(path):
                    self.runbooks_dir = path
                    break
        
        if not self.runbooks_dir:
            logger.error("Runbooks directory not found!")
            
        if cache_path:
            self.cache_path = cache_path
        else:
            self.cache_path = os.path.join(self.runbooks_dir, "runbooks_embeddings.json") if self.runbooks_dir else "./runbooks_embeddings.json"

        # Initialize Google Generative AI Embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001"
        )

    def _get_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _load_cache(self) -> dict:
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading embedding cache: {e}")
        return {}

    def _save_cache(self, cache: dict):
        try:
            with open(self.cache_path, 'w') as f:
                json.dump(cache, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving embedding cache: {e}")

    def sync_runbooks(self):
        if not self.runbooks_dir:
            logger.error("No runbooks directory to sync.")
            return

        cache = self._load_cache()
        updated = False

        for filename in os.listdir(self.runbooks_dir):
            if filename.endswith(".md"):
                filepath = os.path.join(self.runbooks_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                    
                    content_hash = self._get_hash(content)
                    # Check if file has changed or embedding not present
                    if filename not in cache or cache[filename].get("hash") != content_hash:
                        logger.info(f"Embedding runbook: {filename}...")
                        vector = self.embeddings.embed_query(content)
                        cache[filename] = {
                            "hash": content_hash,
                            "content": content,
                            "embedding": vector
                        }
                        updated = True
                except Exception as e:
                    logger.error(f"Failed to process runbook {filename}: {e}")

        # Clean up deleted runbooks from cache
        current_files = {f for f in os.listdir(self.runbooks_dir) if f.endswith(".md")}
        for cached_file in list(cache.keys()):
            if cached_file not in current_files:
                del cache[cached_file]
                updated = True

        if updated:
            self._save_cache(cache)

    def _cosine_similarity(self, vec1, vec2) -> float:
        dot_product = sum(x * y for x, y in zip(vec1, vec2))
        norm_a = math.sqrt(sum(x * x for x in vec1))
        norm_b = math.sqrt(sum(y * y for y in vec2))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    def search_similar(self, query: str, top_k: int = 1) -> list:
        self.sync_runbooks()
        cache = self._load_cache()
        if not cache:
            return []

        try:
            logger.info(f"Embedding query for search: {query[:50]}...")
            query_vector = self.embeddings.embed_query(query)
        except Exception as e:
            logger.error(f"Failed to embed search query: {e}")
            # Fallback: if embedding fails, return all
            return [{"filename": name, "content": info["content"], "similarity": 0.0} for name, info in cache.items()][:top_k]

        results = []
        for filename, doc_info in cache.items():
            sim = self._cosine_similarity(query_vector, doc_info["embedding"])
            results.append({
                "filename": filename,
                "content": doc_info["content"],
                "similarity": sim
            })

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
