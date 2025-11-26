import os
import json
from pathlib import Path
from typing import List, Dict, Tuple
from openai import OpenAI
import hashlib

class DocumentationService:
    def __init__(self, docs_folder: str = "documentation/app_movil"):
        self.docs_folder = Path(docs_folder)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
        self.embeddings_cache_file = "documentation_embeddings.json"
        self.embeddings_cache = self._load_cache()
        
    def _load_cache(self) -> Dict:
        """Carga el caché de embeddings desde archivo"""
        if os.path.exists(self.embeddings_cache_file):
            try:
                with open(self.embeddings_cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        """Guarda el caché de embeddings en archivo"""
        with open(self.embeddings_cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.embeddings_cache, f, ensure_ascii=False, indent=2)
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Genera hash del archivo para detectar cambios"""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def _split_text(self, text: str, chunk_size: int = 1000) -> List[str]:
        """Divide el texto en chunks para procesamiento"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 por el espacio
            if current_length + word_length > chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = word_length
            else:
                current_chunk.append(word)
                current_length += word_length
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def _get_embedding(self, text: str) -> List[float]:
        """Obtiene el embedding de un texto usando OpenAI"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",  # Modelo económico
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error al obtener embedding: {e}")
            return []
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calcula similitud coseno entre dos vectores"""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def load_documents(self) -> List[Dict]:
        """Carga todos los documentos markdown de la carpeta"""
        documents = []
        
        if not self.docs_folder.exists():
            print(f"⚠️ Carpeta de documentación no encontrada: {self.docs_folder}")
            return documents
        
        for md_file in self.docs_folder.glob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                file_hash = self._get_file_hash(md_file)
                cache_key = f"{md_file.name}_{file_hash}"
                
                # Dividir en chunks
                chunks = self._split_text(content)
                
                for i, chunk in enumerate(chunks):
                    chunk_id = f"{md_file.name}_chunk_{i}"
                    
                    # Verificar si ya tenemos el embedding en caché
                    if cache_key in self.embeddings_cache and chunk_id in self.embeddings_cache[cache_key]:
                        embedding = self.embeddings_cache[cache_key][chunk_id]
                    else:
                        # Generar nuevo embedding
                        embedding = self._get_embedding(chunk)
                        
                        # Guardar en caché
                        if cache_key not in self.embeddings_cache:
                            self.embeddings_cache[cache_key] = {}
                        self.embeddings_cache[cache_key][chunk_id] = embedding
                        self._save_cache()
                    
                    documents.append({
                        'id': chunk_id,
                        'file': md_file.name,
                        'content': chunk,
                        'embedding': embedding
                    })
                
                print(f"✅ Cargado: {md_file.name} ({len(chunks)} chunks)")
                
            except Exception as e:
                print(f"❌ Error al cargar {md_file.name}: {e}")
        
        return documents
    
    def search_relevant_docs(self, query: str, documents: List[Dict], top_k: int = 3) -> List[Dict]:
        """Busca los documentos más relevantes para una consulta"""
        if not documents:
            return []
        
        # Obtener embedding de la consulta
        query_embedding = self._get_embedding(query)
        if not query_embedding:
            return []
        
        # Calcular similitud con todos los documentos
        scored_docs = []
        for doc in documents:
            if not doc.get('embedding'):
                continue
            
            similarity = self._cosine_similarity(query_embedding, doc['embedding'])
            scored_docs.append({
                'content': doc['content'],
                'file': doc['file'],
                'score': similarity
            })
        
        # Ordenar por similitud y retornar top_k
        scored_docs.sort(key=lambda x: x['score'], reverse=True)
        return scored_docs[:top_k]

