# IEP RAG System - Project Documentation

## Executive Summary

This project implements a production-ready Retrieval-Augmented Generation (RAG) system for generating IDEA-compliant IEP transition goals. It combines web scraping, semantic search, and large language models to assist special education professionals in creating evidence-based, standards-aligned transition plans.

**Key Achievement**: Automated generation of legally compliant IEP goals that align with both industry standards (BLS Occupational Outlook Handbook) and educational frameworks (21st Century Skills, IDEA 2004).

---

## 1. Problem Statement

### Challenge
Special education teachers must create individualized transition goals that are:
- Measurable and specific
- Based on student assessments and interests
- Aligned with industry/occupational standards
- Compliant with IDEA 2004 legal requirements
- Connected to educational frameworks

This process is time-consuming and requires expertise in:
- Special education law
- Career/occupation requirements
- Assessment interpretation
- Standards alignment

### Solution
A RAG system that:
1. Retrieves relevant career and standards information
2. Generates customized, compliant goals
3. Explains alignment with standards
4. Saves educators time while ensuring quality

---

## 2. Technical Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│                  (Streamlit Web App)                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ├──► Student Information Input
                     ├──► Settings Configuration
                     └──► Goal Display & Download
                     
┌─────────────────────────────────────────────────────────┐
│                   RAG Pipeline                           │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   ┌────────┐  ┌─────────┐  ┌─────────┐
   │Embedder│  │ FAISS   │  │Retriever│
   │        │  │ Index   │  │         │
   └────────┘  └─────────┘  └─────────┘
   
┌─────────────────────────────────────────────────────────┐
│                Knowledge Base                            │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬──────────────┐
        │            │            │              │
        ▼            ▼            ▼              ▼
    ┌──────┐   ┌─────────┐  ┌────────┐    ┌─────────┐
    │ BLS  │   │  Iowa   │  │ IDEA   │    │   IEP   │
    │ OOH  │   │Standards│  │  2004  │    │Examples │
    └──────┘   └─────────┘  └────────┘    └─────────┘
    
┌─────────────────────────────────────────────────────────┐
│              Goal Generation (GPT-4)                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
              Structured Goals
```

### Data Flow

1. **User Input** → Student profile and preferences
2. **Retrieval** → Semantic search for relevant documents
3. **Context Formation** → Combine retrieved information
4. **Prompt Construction** → Build structured prompt with context
5. **Generation** → GPT-4 creates goals
6. **Parsing** → Extract structured components
7. **Display** → Present to user with formatting

---

## 3. Implementation Details

### 3.1 Data Collection (`src/data_collection.py`)

**BLS Scraping:**
- Target: 8 occupations (retail, food service, office, warehouse, etc.)
- Method: BeautifulSoup web scraping
- Caching: JSON files to avoid repeated requests
- Sections: Duties, training, environment, requirements

**Standards Loading:**
- Iowa 21st Century Skills (4 categories, 20+ standards)
- IDEA 2004 requirements (6 key requirements)
- Manual curation for accuracy

**Sample Goals:**
- 7 example IEP goals
- Different types: employment, training, annual, short-term
- Metadata: type, context, target population

**Output:** `data/knowledge_base.pkl` with 100+ documents

### 3.2 RAG Pipeline (`src/rag_pipeline.py`)

**Embedding Model:**
- Model: `all-MiniLM-L6-v2` (sentence-transformers)
- Rationale: Fast, accurate for semantic similarity
- Dimension: 384
- Normalization: L2 normalized for cosine similarity

**Chunking Strategy:**
- Size: 512 characters
- Overlap: 50 characters
- Method: Recursive character splitting
- Preserves: Complete sentences when possible

**Vector Store:**
- Engine: FAISS (Facebook AI Similarity Search)
- Index Type: IndexFlatIP (inner product)
- Metadata: Source, section, category preserved

**Retrieval:**
- Multi-query approach:
  - Occupation query: "duties requirements for [interest]"
  - Standards query: "employability skills for [interest]"
  - Examples query: "IEP goal [interest] employment"
- Top-K: 5 per category (15 total max)
- Deduplication: Remove redundant chunks

### 3.3 Prompt Engineering (`src/goal_generator.py`)

**System Prompt:**
```
Role: Expert special education transition specialist
Knowledge: IDEA 2004, IEP development, career pathways
Task: Generate measurable, compliant goals
```

**User Prompt Structure:**
1. Student Information (name, age, interests, assessment)
2. Retrieved Context (occupation info, standards, examples)
3. Output Requirements (postsecondary goals, annual objective, short-term objectives, alignment)
4. Formatting Instructions

**Key Design Decisions:**
- Explicit output structure (numbered sections)
- Measurability requirements stated
- Examples of good criteria (e.g., "4 out of 5 opportunities")
- Student-specific personalization
- Standards citation requirement

**Generation Parameters:**
- Model: GPT-4 (or GPT-3.5-turbo)
- Temperature: 0.7 (balanced creativity/consistency)
- Max tokens: 2000
- Top-p: 1.0

### 3.4 User Interface (`app.py`)

**Framework:** Streamlit (rapid prototyping, easy deployment)

**Layout:**
- Sidebar: Input forms and settings
- Main area: Two columns (input summary, context preview)
- Output: Expandable sections by category
- Footer: Download and refinement options

**Features:**
- Sample data loading (Clarence case study)
- Context preview (see what's retrieved)
- Real-time generation feedback
- Structured output display
- Download as text file
- Refinement workflow (session state)

**State Management:**
- Session state for generated goals
- Caching for RAG system loading
- API key persistence

---

## 4. Evaluation

### 4.1 Functionality Assessment

**Test Case: Clarence (15yo, interested in retail)**

Generated Output Quality:
-  Postsecondary employment goal: Specific, measurable, realistic
-  Postsecondary training goal: Appropriate for occupation
-  Annual objective: Measurable criteria, timeline, skills-focused
-  Short-term objectives: Progressive, building toward annual goal
-  Standards alignment: Explicit citations, clear connections

**IDEA 2004 Compliance:**
-  Measurable postsecondary goals
-  Based on age-appropriate assessments
-  Reflects student interests
-  Includes necessary services/courses

**Strengths:**
1. Consistent structure across generations
2. Appropriate vocabulary for student age
3. Realistic timelines (36 weeks, 12 weeks, etc.)
4. Clear measurement criteria
5. Good alignment explanations

**Areas for Improvement:**
1. Sometimes overly generic language
2. May need refinement for complex disabilities
3. Limited to available occupation data

### 4.2 Technical Performance

**Data Collection:**
- BLS scraping: ~5-10 minutes for 8 occupations
- Standards loading: <1 second
- Knowledge base: 100+ documents

**Embedding & Indexing:**
- Embedding generation: ~30 seconds for 100+ chunks
- Index building: <5 seconds
- Index size: ~50KB

**Retrieval:**
- Query time: <100ms
- Relevance: High (manual spot-checking)
- Coverage: Good for supported occupations

**Generation:**
- Latency: 20-40 seconds (GPT-4)
- Cost: ~$0.10-0.20 per generation
- Quality: Consistently high

**UI Performance:**
- Load time: ~5 seconds (embedding model)
- Responsiveness: Good
- Caching: Effective

### 4.3 User Experience

**Positive Aspects:**
- Simple, intuitive interface
- Clear instructions
- Sample data helpful for learning
- Structured output easy to read
- Download functionality useful

**Challenges:**
- Requires OpenAI API key (cost barrier)
- Generation wait time (30-60s)
- Limited occupation coverage
- No offline mode

---

## 5. Challenges & Solutions

### Challenge 1: Web Scraping Reliability
**Problem:** BLS website structure may change  
**Solution:** 
- Caching to minimize requests
- Error handling for missing sections
- Manual fallback data

### Challenge 2: Retrieval Quality
**Problem:** Generic queries return irrelevant docs  
**Solution:**
- Multi-query approach
- Source filtering
- Metadata preservation for context

### Challenge 3: Goal Measurability
**Problem:** LLMs sometimes generate vague goals  
**Solution:**
- Explicit prompt instructions
- Examples of good criteria
- Temperature tuning (0.7)

### Challenge 4: Standards Alignment
**Problem:** Vague connections to standards  
**Solution:**
- Include full standard text in context
- Require explicit citation in prompt
- Provide examples of good alignment

### Challenge 5: API Cost
**Problem:** OpenAI API has per-use cost  
**Solution:**
- Efficient prompting (concise context)
- Option for GPT-3.5-turbo (cheaper)
- Future: Local LLM support

---

## 6. Future Improvements

### Short-term (1-3 months)
1. **Expand Occupations**: Add 20+ more BLS occupations
2. **Multi-State Standards**: Support CA, TX, FL standards
3. **PDF Export**: Professional formatting with school letterhead
4. **Assessment Integration**: Direct O*Net API connection
5. **User Feedback**: Rating system for generated goals

### Medium-term (3-6 months)
1. **Compliance Checker**: Automated IDEA validation
2. **Historical Learning**: Track successful goals
3. **Multi-Language**: Spanish support
4. **Collaboration**: Teacher comments and version history
5. **Progress Monitoring**: Link to data collection tools

### Long-term (6-12 months)
1. **Local LLM**: Llama/Mistral for privacy
2. **Fine-tuning**: Custom model on IEP corpus
3. **Mobile App**: iOS/Android version
4. **District Integration**: Connect to student information systems
5. **Analytics Dashboard**: Usage statistics, outcome tracking

---

## 7. Lessons Learned

### Technical Insights
1. **RAG is powerful**: Grounding in real data dramatically improves quality
2. **Prompt engineering matters**: Explicit structure >>> implicit expectations
3. **Chunking strategy**: 512 chars with overlap works well for this domain
4. **Caching is essential**: Saves time and respects external services

### Product Insights
1. **Sample data crucial**: Users need examples to understand
2. **Show your work**: Context preview builds trust
3. **Refinement needed**: One-shot rarely perfect
4. **Download matters**: Users want to save work

### Domain Insights
1. **Compliance is complex**: Many nuanced requirements
2. **Personalization hard**: Balance templates vs. individuality
3. **Standards overwhelming**: Need smart filtering/selection
4. **Educators need tools**: This problem is real and underserved

---

## 8. Conclusion

This project successfully demonstrates a production-ready RAG system for IEP goal generation that:

 **Works**: Generates high-quality, compliant goals  
 **Scales**: Handles various student profiles and interests  
 **Educates**: Provides transparency through context and alignment  
 **Saves Time**: Automates time-consuming research and writing  

The system could genuinely help special education professionals create better IEP goals more efficiently, while maintaining the required legal compliance and educational quality.

**Key Takeaway**: RAG systems excel when domain knowledge is scattered across multiple sources and needs to be synthesized with personalized information—exactly the challenge in IEP development.

---

## Appendix A: File Structure

```
NLP/
├── app.py                      # Main Streamlit application (348 lines)
├── requirements.txt            # Dependencies
├── .env.example               # Environment template
├── README.md                  # Full documentation
├── QUICKSTART.md             # Quick start guide
├── PROJECT_DOCS.md           # This file
├── test_setup.py             # Installation test script
│
├── src/
│   ├── data_collection.py    # BLS scraping, standards loading (297 lines)
│   ├── rag_pipeline.py       # Embeddings, FAISS, retrieval (336 lines)
│   └── goal_generator.py     # Prompts, GPT generation (274 lines)
│
├── data/                     # Generated data files
│   ├── knowledge_base.pkl    # Combined documents
│   ├── iep_faiss.index      # Vector index
│   ├── iep_metadata.pkl     # Document metadata
│   └── scraped/             # Cached BLS data
│
└── rag_iep_project_template.ipynb  # Original notebook

Total: ~1,255 lines of production code
```

## Appendix B: Key Technologies

| Technology | Purpose | Why Chosen |
|-----------|---------|-----------|
| **sentence-transformers** | Text embedding | State-of-art semantic similarity |
| **FAISS** | Vector search | Fast, scalable, production-ready |
| **BeautifulSoup** | Web scraping | Reliable HTML parsing |
| **OpenAI GPT-4** | Goal generation | Best-in-class language model |
| **Streamlit** | Web interface | Rapid prototyping, easy deployment |
| **LangChain** | Text chunking | Industry-standard utilities |

## Appendix C: Data Statistics

- **Occupations**: 8 from BLS OOH
- **Standards**: 20+ from Iowa framework
- **IDEA Requirements**: 6 key requirements
- **Sample Goals**: 7 examples
- **Total Documents**: 100+ in knowledge base
- **Vector Dimensions**: 384
- **Average Chunk Size**: ~400 characters
- **Index Size**: ~50KB

---

**Document Version**: 1.0  
**Last Updated**: 2025  
**Authors**: Samuel Terkper Kwasi Tetteh
