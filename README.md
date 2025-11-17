# IEP Transition Goal Generator

A Retrieval-Augmented Generation (RAG) system for generating IDEA-compliant IEP transition goals for students with disabilities, aligned with industry standards and educational frameworks.

## 🎯 Overview

This system assists special education professionals in creating comprehensive, measurable IEP transition goals by:
- Retrieving relevant career information from the Bureau of Labor Statistics Occupational Outlook Handbook
- Aligning goals with educational standards (21st Century Skills, employability frameworks)
- Generating legally compliant postsecondary goals and objectives
- Providing evidence-based alignment with industry requirements

## ✨ Features

- **Smart Retrieval**: RAG pipeline using FAISS vector search and sentence transformers
- **Standards Alignment**: Automatic alignment with Iowa 21st Century Skills and IDEA 2004 requirements
- **Career-Focused**: Integration with BLS Occupational Outlook Handbook for current job market data
- **User-Friendly Interface**: Streamlit web application with intuitive input forms
- **Customizable**: Adjustable generation parameters and refinement options
- **Export Ready**: Download generated goals in text format

## 📋 Requirements

- Python 3.8+
- OpenAI API key (for GPT-4 or GPT-3.5-turbo)
- Internet connection (for initial data collection)

## 🚀 Installation

### 1. Clone or Download the Project

```bash
cd /path/to/NLP
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4
```

## 📊 Data Collection & Setup

### Step 1: Collect Data

Run the data collection script to scrape BLS data and build the knowledge base:

```bash
python src/data_collection.py
```

This will:
- Scrape occupation data from the BLS Occupational Outlook Handbook
- Load educational standards (Iowa 21st Century Skills, IDEA requirements)
- Compile sample IEP goals
- Save everything to `data/knowledge_base.pkl`

**Note**: This step may take 5-10 minutes depending on your internet connection.

### Step 2: Build Vector Index

Build the FAISS vector index for retrieval:

```bash
python src/rag_pipeline.py
```

This will:
- Generate embeddings using `all-MiniLM-L6-v2`
- Build FAISS index for semantic search
- Save index to `data/iep_faiss.index` and metadata to `data/iep_metadata.pkl`

## 🎮 Usage

### Running the Application

Start the Streamlit web interface:

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Using the Interface

1. **Enter Student Information** (left sidebar):
   - Student name, age, and grade
   - Career interests (e.g., "retail sales", "food service")
   - Assessment results (e.g., O*Net Interest Profiler scores)
   - Additional notes

2. **Optional: Use Sample Data**:
   - Check "Use Sample Data (Clarence)" to load the example case study

3. **Preview Retrieved Context** (optional):
   - Click to see what information the system retrieves for the student

4. **Configure Settings**:
   - Enter OpenAI API key (or set in `.env`)
   - Choose model (GPT-4 recommended for best quality)
   - Adjust creativity/temperature

5. **Generate Goals**:
   - Click "Generate IEP Goals"
   - Wait 30-60 seconds for generation
   - Review generated goals organized by category

6. **Refine Goals** (optional):
   - Provide feedback for refinement
   - Generate revised version

7. **Download**:
   - Click "Download Goals as Text" to save

### Sample Case: Clarence

The system includes a pre-loaded example:

**Student Profile:**
- Name: Clarence
- Age: 15, Grade 10
- Interests: Retail sales, working at Walmart
- Assessment: Strong in Enterprising (O*Net)

**Expected Output:**
- Postsecondary employment goal (e.g., full-time retail position at Walmart)
- Postsecondary training goal (on-the-job training, customer service workshops)
- Annual IEP objective (workplace communication and customer service skills)
- 3-4 short-term objectives with measurable criteria
- Alignment with BLS standards and 21st Century Skills

## 📁 Project Structure

```
NLP/
├── app.py                          # Streamlit web application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore file
├── README.md                       # This file
│
├── src/
│   ├── data_collection.py         # BLS scraping & knowledge base building
│   ├── rag_pipeline.py             # Embeddings, FAISS, retrieval
│   └── goal_generator.py           # Prompt engineering & GPT generation
│
├── data/
│   ├── knowledge_base.pkl          # Combined knowledge base (generated)
│   ├── iep_faiss.index             # FAISS vector index (generated)
│   ├── iep_metadata.pkl            # Document metadata (generated)
│   └── scraped/                    # Cached BLS occupation data (generated)
│
└── rag_iep_project_template.ipynb  # Original Jupyter notebook
```

## 🔧 Technical Implementation

### Data Collection & Preprocessing

**Sources:**
- **BLS Occupational Outlook Handbook**: 8+ key occupations (retail, food service, office work, etc.)
- **Iowa 21st Century Skills**: Employability, communication, critical thinking standards
- **IDEA 2004 Requirements**: Transition planning legal requirements
- **Sample IEP Goals**: 7+ example transition goals and objectives

**Processing:**
- Web scraping with BeautifulSoup
- Caching to avoid repeated requests
- Structured metadata preservation

### RAG Pipeline

**Embedding:**
- Model: `all-MiniLM-L6-v2` (sentence-transformers)
- Dimension: 384
- Normalized embeddings for cosine similarity

**Vector Store:**
- FAISS IndexFlatIP (inner product for cosine similarity)
- Chunking: 512 characters with 50-character overlap
- Metadata tracking for source attribution

**Retrieval Strategy:**
- Multi-query approach (occupation, standards, examples)
- Source-based filtering
- Top-5 results per category
- Context formatting for prompt inclusion

### Prompt Engineering

**System Prompt:**
- Expert persona in special education transition planning
- IDEA 2004 compliance focus
- Measurability and standards alignment emphasis

**User Prompt Structure:**
1. Student information section
2. Retrieved context (occupation, standards, examples)
3. Structured output requirements
4. Explicit formatting instructions

**Generation:**
- OpenAI GPT-4 or GPT-3.5-turbo
- Temperature: 0.7 (balanced creativity/consistency)
- Max tokens: 2000
- Refinement support via conversation history

### User Interface

**Streamlit Components:**
- Sidebar for student input and settings
- Two-column layout for input summary and context preview
- Expandable sections for detailed output
- Session state for refinement workflow
- Download functionality

## 📈 Evaluation & Results

### Strengths

✅ **Accuracy**: Generates IDEA-compliant, measurable goals  
✅ **Alignment**: Successfully connects to relevant standards and occupation requirements  
✅ **Usability**: Intuitive interface for educators without technical expertise  
✅ **Flexibility**: Supports various career interests and student profiles  
✅ **Evidence-Based**: Grounded in current occupation data and best practices  

### Limitations

⚠️ **API Dependency**: Requires OpenAI API (cost per generation)  
⚠️ **Coverage**: Limited to 8 occupation categories (expandable)  
⚠️ **Standards Scope**: Currently Iowa-focused (can add other states)  
⚠️ **Validation**: No automated compliance checking  
⚠️ **Personalization**: May need refinement for complex cases  

### Potential Improvements

1. **Expand Occupation Coverage**: Add more BLS occupations based on usage patterns
2. **Multi-State Standards**: Include standards from multiple states
3. **Compliance Checker**: Automated validation against IDEA requirements
4. **Historical Data**: Track and learn from previously generated goals
5. **Assessment Integration**: Direct O*Net API integration
6. **PDF Export**: Formatted PDF output with school letterhead
7. **Multi-Language**: Support for Spanish and other languages
8. **Offline Mode**: Local LLM support (Llama, Mistral) for privacy
9. **Progress Monitoring**: Link to data collection tools
10. **Collaboration**: Multi-user support with teacher comments

## 🧪 Testing

### Manual Testing

1. Run with sample data (Clarence)
2. Test with various career interests
3. Validate retrieval context relevance
4. Review goal quality and alignment
5. Test refinement functionality

### Automated Testing (Future)

```bash
# Unit tests
pytest tests/

# Integration tests
pytest tests/integration/
```

## 📚 Resources

- **BLS Occupational Outlook Handbook**: https://www.bls.gov/ooh/
- **Iowa 21st Century Skills**: https://educate.iowa.gov/
- **IDEA 2004 Transition Requirements**: https://sites.ed.gov/idea/
- **LangChain Documentation**: https://python.langchain.com/
- **Sentence Transformers**: https://www.sbert.net/

## 🤝 Contributing

This is an educational project. Suggestions for improvement:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## ⚖️ Legal & Compliance

**Important Notes:**
- This tool assists in goal creation but does not replace professional judgment
- All goals should be reviewed by qualified special education professionals
- Ensure compliance with local, state, and federal regulations
- Student data privacy must be maintained (do not share personal information)

**IDEA 2004 Compliance:**
- Goals are generated to meet measurability requirements
- Based on age-appropriate transition assessments
- Aligned with student strengths, preferences, and interests
- Include necessary transition services

## 📞 Support

For issues or questions:
1. Check the documentation above
2. Review error messages carefully
3. Ensure all dependencies are installed
4. Verify API key is valid
5. Check that data collection and indexing completed successfully

## 📄 License

This project is for educational purposes. Use responsibly and in compliance with all applicable laws and regulations.

## 🙏 Acknowledgments

- Bureau of Labor Statistics for occupation data
- OpenAI for language model API
- Iowa Department of Education for standards framework
- Special education professionals who inspired this project

---

**Version**: 1.0.0  
**Last Updated**: 2025  
**Author**: RAG IEP Project Team
