l -9 python
"""
RAG Pipeline Module for IEP Goal Generation
Handles embeddings, vector storage, and retrieval
"""

import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter


class EmbeddingManager:
    """Manages document embeddings using SentenceTransformers"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Initialize embedding model
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
    
    def embed_documents(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of documents
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            Numpy array of embeddings
        """
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
            batch_size=32
        )
        return embeddings.astype('float32')
    
    def embed_query(self, query: str) -> np.ndarray:
        """Generate embedding for a single query
        
        Args:
            query: Query text
            
        Returns:
            Numpy array embedding
        """
        embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )
        return embedding.astype('float32')


class DocumentChunker:
    """Chunks documents for optimal retrieval"""
    
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        """Initialize chunker
        
        Args:
            chunk_size: Maximum size of each chunk
            chunk_overlap: Overlap between chunks
        """
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def chunk_documents(self, documents: List[Dict[str, str]]) -> Tuple[List[str], List[Dict]]:
        """Chunk documents and preserve metadata
        
        Args:
            documents: List of document dictionaries with 'text' and metadata
            
        Returns:
            Tuple of (chunked_texts, metadata_list)
        """
        chunked_texts = []
        metadata_list = []
        
        for doc in documents:
            text = doc['text']
            chunks = self.splitter.split_text(text)
            
            for chunk in chunks:
                chunked_texts.append(chunk)
                # Preserve metadata for each chunk
                metadata_list.append({
                    **{k: v for k, v in doc.items() if k != 'text'},
                    'chunk_text': chunk
                })
        
        return chunked_texts, metadata_list


class VectorStore:
    """FAISS-based vector store for document retrieval"""
    
    def __init__(self, embedding_manager: EmbeddingManager):
        """Initialize vector store
        
        Args:
            embedding_manager: EmbeddingManager instance
        """
        self.embedding_manager = embedding_manager
        self.index = None
        self.metadata = None
        self.dimension = embedding_manager.embedding_dim
    
    def build_index(self, documents: List[Dict[str, str]], chunk_size: int = 512):
        """Build FAISS index from documents
        
        Args:
            documents: List of document dictionaries
            chunk_size: Size for chunking documents
        """
        print("Chunking documents...")
        chunker = DocumentChunker(chunk_size=chunk_size)
        texts, metadata = chunker.chunk_documents(documents)
        
        print(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self.embedding_manager.embed_documents(texts)
        
        print("Building FAISS index...")
        # Use IndexFlatIP for inner product (cosine similarity with normalized vectors)
        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(embeddings)
        
        self.metadata = metadata
        print(f"Index built with {self.index.ntotal} vectors")
    
    def save(self, index_path: str = 'data/iep_faiss.index', 
             metadata_path: str = 'data/iep_metadata.pkl'):
        """Save index and metadata to disk
        
        Args:
            index_path: Path to save FAISS index
            metadata_path: Path to save metadata
        """
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        faiss.write_index(self.index, index_path)
        
        with open(metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
        
        print(f"Saved index to {index_path} and metadata to {metadata_path}")
    
    def load(self, index_path: str = 'data/iep_faiss.index',
             metadata_path: str = 'data/iep_metadata.pkl'):
        """Load index and metadata from disk
        
        Args:
            index_path: Path to FAISS index
            metadata_path: Path to metadata
        """
        self.index = faiss.read_index(index_path)
        
        with open(metadata_path, 'rb') as f:
            self.metadata = pickle.load(f)
        
        print(f"Loaded index with {self.index.ntotal} vectors")
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for relevant documents
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of metadata dictionaries for top k results
        """
        if self.index is None:
            raise ValueError("Index not built or loaded")
        
        query_embedding = self.embedding_manager.embed_query(query)
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.metadata):
                result = self.metadata[idx].copy()
                result['similarity_score'] = float(distances[0][i])
                results.append(result)
        
        return results


class ContextRetriever:
    """High-level retriever that combines different search strategies"""
    
    def __init__(self, vector_store: VectorStore):
        """Initialize retriever
        
        Args:
            vector_store: VectorStore instance
        """
        self.vector_store = vector_store
    
    def retrieve_for_student(self, student_info: Dict[str, str], 
                            top_k: int = 10) -> Dict[str, List[Dict]]:
        """Retrieve relevant context for a student
        
        Args:
            student_info: Dictionary with student information
            top_k: Number of documents to retrieve per category
            
        Returns:
            Dictionary with categorized retrieved documents
        """
        results = {
            'occupation_info': [],
            'standards': [],
            'examples': [],
        }
        
        # Build search queries based on student interests
        interests = student_info.get('interests', '')
        assessment = student_info.get('assessment', '')
        
        # Search for occupation information
        occupation_query = f"occupation duties requirements training for {interests}"
        occupation_docs = self.vector_store.search(occupation_query, k=top_k)
        results['occupation_info'] = [
            doc for doc in occupation_docs 
            if doc.get('source') == 'BLS_OOH'
        ]
        
        # Search for relevant standards
        standards_query = f"employability skills communication workplace behavior for {interests}"
        standards_docs = self.vector_store.search(standards_query, k=top_k)
        results['standards'] = [
            doc for doc in standards_docs 
            if doc.get('source') in ['Iowa_Standards', 'IDEA_2004']
        ]
        
        # Search for example goals
        examples_query = f"IEP transition goal {interests} employment training"
        example_docs = self.vector_store.search(examples_query, k=top_k)
        results['examples'] = [
            doc for doc in example_docs 
            if doc.get('source') == 'IEP_Examples'
        ]
        
        # Also get general IDEA requirements
        idea_docs = [
            doc for doc in self.vector_store.metadata
            if doc.get('source') == 'IDEA_2004'
        ]
        results['standards'].extend(idea_docs[:3])
        
        # Remove duplicates while preserving order
        for key in results:
            seen = set()
            unique_results = []
            for doc in results[key]:
                doc_id = doc.get('chunk_text', '')
                if doc_id not in seen:
                    seen.add(doc_id)
                    unique_results.append(doc)
            results[key] = unique_results[:5]  # Limit to top 5 per category
        
        return results
    
    def format_context_for_prompt(self, retrieved_docs: Dict[str, List[Dict]]) -> str:
        """Format retrieved documents for inclusion in prompt
        
        Args:
            retrieved_docs: Dictionary of categorized documents
            
        Returns:
            Formatted string for prompt
        """
        context_parts = []
        
        if retrieved_docs['occupation_info']:
            context_parts.append("=== Career Information ===")
            for doc in retrieved_docs['occupation_info'][:3]:
                context_parts.append(f"- {doc['chunk_text']}")
        
        if retrieved_docs['standards']:
            context_parts.append("\n=== Relevant Standards ===")
            for doc in retrieved_docs['standards'][:3]:
                context_parts.append(f"- {doc['chunk_text']}")
        
        if retrieved_docs['examples']:
            context_parts.append("\n=== Example IEP Goals ===")
            for doc in retrieved_docs['examples'][:2]:
                context_parts.append(f"- {doc['chunk_text']}")
        
        return "\n".join(context_parts)


def build_and_save_index(documents: List[Dict[str, str]]):
    """Build and save vector index from documents
    
    Args:
        documents: List of document dictionaries
    """
    embedding_manager = EmbeddingManager()
    vector_store = VectorStore(embedding_manager)
    vector_store.build_index(documents)
    vector_store.save()
    return vector_store


if __name__ == "__main__":
    # Test the RAG pipeline
    print("Loading knowledge base...")
    with open('data/knowledge_base.pkl', 'rb') as f:
        documents = pickle.load(f)
    
    print(f"\nBuilding index from {len(documents)} documents...")
    vector_store = build_and_save_index(documents)
    
    # Test retrieval
    print("\n" + "="*50)
    print("Testing retrieval...")
    retriever = ContextRetriever(vector_store)
    
    test_student = {
        'name': 'Clarence',
        'age': 15,
        'grade': '10',
        'interests': 'retail sales',
        'assessment': 'Strong in Enterprising activities'
    }
    
    results = retriever.retrieve_for_student(test_student)
    
    print(f"\nRetrieved {len(results['occupation_info'])} occupation docs")
    print(f"Retrieved {len(results['standards'])} standards docs")
    print(f"Retrieved {len(results['examples'])} example docs")
    
    print("\n=== Sample Retrieved Context ===")
    print(retriever.format_context_for_prompt(results)[:500] + "...")
