"""
Test script for IEP RAG System
Run this to verify installation and test basic functionality
"""

import os
import sys


def test_imports():
    """Test that all required packages are installed"""
    print("Testing imports...")
    
    try:
        import requests
        print("✓ requests")
    except ImportError:
        print("✗ requests - run: pip install requests")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✓ beautifulsoup4")
    except ImportError:
        print("✗ beautifulsoup4 - run: pip install beautifulsoup4")
        return False
    
    try:
        from sentence_transformers import SentenceTransformer
        print("✓ sentence-transformers")
    except ImportError:
        print("✗ sentence-transformers - run: pip install sentence-transformers")
        return False
    
    try:
        import faiss
        print("✓ faiss-cpu")
    except ImportError:
        print("✗ faiss-cpu - run: pip install faiss-cpu")
        return False
    
    try:
        import numpy as np
        print("✓ numpy")
    except ImportError:
        print("✗ numpy - run: pip install numpy")
        return False
    
    try:
        import streamlit
        print("✓ streamlit")
    except ImportError:
        print("✗ streamlit - run: pip install streamlit")
        return False
    
    try:
        import openai
        print("✓ openai")
    except ImportError:
        print("✗ openai - run: pip install openai")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✓ python-dotenv")
    except ImportError:
        print("✗ python-dotenv - run: pip install python-dotenv")
        return False
    
    print("\n✅ All required packages are installed!\n")
    return True


def test_data_structure():
    """Test that necessary directories exist"""
    print("Checking directory structure...")
    
    required_dirs = ['data', 'src']
    required_files = ['src/data_collection.py', 'src/rag_pipeline.py', 
                     'src/goal_generator.py', 'app.py']
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✓ {dir_name}/ exists")
        else:
            print(f"✗ {dir_name}/ missing")
            os.makedirs(dir_name, exist_ok=True)
            print(f"  Created {dir_name}/")
    
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✓ {file_name} exists")
        else:
            print(f"✗ {file_name} missing")
    
    print()


def test_env_setup():
    """Test environment configuration"""
    print("Checking environment configuration...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    
    if api_key and api_key != 'your_openai_api_key_here':
        print("✓ OPENAI_API_KEY is set")
        print(f"  Key: {api_key[:8]}...{api_key[-4:]}")
    else:
        print("⚠ OPENAI_API_KEY not set or using placeholder")
        print("  You'll need to set this in .env or provide it in the UI")
    
    print()


def test_data_collection():
    """Test data collection functionality"""
    print("Testing data collection...")
    
    try:
        from src.data_collection import EducationalStandardsLoader, IEPExamplesLoader
        
        # Test standards loading
        loader = EducationalStandardsLoader()
        standards = loader.get_all_standards()
        
        print(f"✓ Loaded {len(standards['iowa_standards'])} standard categories")
        print(f"✓ Loaded {len(standards['idea_requirements'])} IDEA requirements")
        
        # Test examples loading
        examples = IEPExamplesLoader.load_sample_goals()
        print(f"✓ Loaded {len(examples)} sample IEP goals")
        
        print()
        return True
        
    except Exception as e:
        print(f"✗ Error in data collection: {str(e)}")
        return False


def test_embedding():
    """Test embedding model"""
    print("Testing embedding model (this may take a moment)...")
    
    try:
        from src.rag_pipeline import EmbeddingManager
        
        manager = EmbeddingManager()
        print(f"✓ Loaded embedding model")
        print(f"  Dimension: {manager.embedding_dim}")
        
        # Test embedding
        test_text = "This is a test sentence for embedding."
        embedding = manager.embed_query(test_text)
        print(f"✓ Generated test embedding: shape {embedding.shape}")
        
        print()
        return True
        
    except Exception as e:
        print(f"✗ Error with embeddings: {str(e)}")
        print(f"  You may need to run: pip install sentence-transformers")
        return False


def check_existing_index():
    """Check if vector index exists"""
    print("Checking for existing vector index...")
    
    if os.path.exists('data/iep_faiss.index') and os.path.exists('data/iep_metadata.pkl'):
        print("✓ Vector index found")
        
        import pickle
        with open('data/iep_metadata.pkl', 'rb') as f:
            metadata = pickle.load(f)
        print(f"  Contains {len(metadata)} document chunks")
        return True
    else:
        print("⚠ Vector index not found")
        print("  Run: python src/data_collection.py")
        print("  Then: python src/rag_pipeline.py")
        return False
    
    print()


def main():
    """Run all tests"""
    print("="*60)
    print("IEP RAG System - Installation & Setup Test")
    print("="*60)
    print()
    
    # Change to project directory if needed
    if not os.path.exists('app.py'):
        print("⚠ Please run this script from the project root directory")
        print("  cd /path/to/NLP")
        return
    
    results = []
    
    # Run tests
    results.append(("Package Installation", test_imports()))
    test_data_structure()
    test_env_setup()
    results.append(("Data Collection", test_data_collection()))
    results.append(("Embedding Model", test_embedding()))
    check_existing_index()
    
    # Summary
    print("="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print()
    
    if all(passed for _, passed in results):
        print("🎉 All tests passed! You're ready to run the application.")
        print()
        print("Next steps:")
        print("1. If you haven't already, collect data:")
        print("   python src/data_collection.py")
        print()
        print("2. Build the vector index:")
        print("   python src/rag_pipeline.py")
        print()
        print("3. Run the application:")
        print("   streamlit run app.py")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
        print()
        print("Common fixes:")
        print("- Install missing packages: pip install -r requirements.txt")
        print("- Check Python version: python --version (need 3.8+)")
        print("- Verify you're in the correct directory")


if __name__ == "__main__":
    main()
