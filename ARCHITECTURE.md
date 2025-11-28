# IEP RAG System - Architecture Diagrams

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER                                     │
│                     (Special Ed Teacher)                         │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ Enters student info & interests
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STREAMLIT WEB UI (app.py)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Input Form   │  │   Settings   │  │  Output      │         │
│  │ • Name       │  │ • API Key    │  │  Display     │         │
│  │ • Age/Grade  │  │ • Model      │  │ • Goals      │         │
│  │ • Interests  │  │ • Temp       │  │ • Alignment  │         │
│  │ • Assessment │  │              │  │ • Download   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ Student profile
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│              RAG PIPELINE (rag_pipeline.py)                      │
│                                                                  │
│  ┌────────────────────────────────────────────────────┐        │
│  │        1. RETRIEVAL                                 │        │
│  │  ┌──────────────┐         ┌──────────────┐        │        │
│  │  │   Query      │────────▶│   FAISS      │        │        │
│  │  │  Builder     │         │   Index      │        │        │
│  │  │              │◀────────│  (384-dim)   │        │        │
│  │  └──────────────┘         └──────────────┘        │        │
│  │         │                         │                 │        │
│  │         │                         │ Top-5/category  │        │
│  │         ▼                         ▼                 │        │
│  │  ┌──────────────────────────────────────┐         │        │
│  │  │   Retrieved Context:                 │         │        │
│  │  │   • Occupation info (BLS)            │         │        │
│  │  │   • Standards (Iowa, IDEA)           │         │        │
│  │  │   • Example goals                    │         │        │
│  │  └──────────────────────────────────────┘         │        │
│  └────────────────────────────────────────────────────┘        │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ Context + Student Info
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│           GOAL GENERATION (goal_generator.py)                    │
│                                                                  │
│  ┌────────────────────────────────────────────────────┐        │
│  │        2. PROMPT ENGINEERING                        │        │
│  │  ┌──────────────────────────────────────┐         │        │
│  │  │  System Prompt (Expert Persona)      │         │        │
│  │  └──────────────────────────────────────┘         │        │
│  │                    +                                │        │
│  │  ┌──────────────────────────────────────┐         │        │
│  │  │  User Prompt:                        │         │        │
│  │  │  • Student information               │         │        │
│  │  │  • Retrieved context                 │         │        │
│  │  │  • Output structure requirements     │         │        │
│  │  └──────────────────────────────────────┘         │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                  │
│  ┌────────────────────────────────────────────────────┐        │
│  │        3. GENERATION                                │        │
│  │  ┌──────────────────────────────────────┐         │        │
│  │  │      OpenAI GPT-4 API                │         │        │
│  │  │      Temperature: 0.7                │         │        │
│  │  │      Max Tokens: 2000                │         │        │
│  │  └──────────────────────────────────────┘         │        │
│  └────────────────────────────────────────────────────┘        │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ Generated goals
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STRUCTURED OUTPUT                             │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ 1. Postsecondary Goals                               │      │
│  │    • Employment goal                                  │      │
│  │    • Training/education goal                         │      │
│  │                                                       │      │
│  │ 2. Annual IEP Objective                              │      │
│  │    • Measurable criteria (e.g., 4/5 opportunities)   │      │
│  │    • Timeline (36 weeks)                             │      │
│  │                                                       │      │
│  │ 3. Short-term Objectives (3-4)                       │      │
│  │    • Progressive skill building                      │      │
│  │    • Specific timelines                              │      │
│  │                                                       │      │
│  │ 4. Standards Alignment                               │      │
│  │    • BLS occupation requirements                     │      │
│  │    • 21st Century Skills                             │      │
│  │    • IDEA 2004 compliance                            │      │
│  └──────────────────────────────────────────────────────┘      │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ Display & Download
                 ▼
              [ USER ]
```

---

## Data Flow Diagram

```
START
  │
  ├─▶ [Data Collection Phase]
  │     │
  │     ├─▶ Scrape BLS OOH (8 occupations)
  │     │     └─▶ Cache to data/scraped/*.json
  │     │
  │     ├─▶ Load Iowa Standards (20+ skills)
  │     │
  │     ├─▶ Load IDEA Requirements (6 items)
  │     │
  │     ├─▶ Load Sample IEP Goals (7 examples)
  │     │
  │     └─▶ Combine → data/knowledge_base.pkl (100+ docs)
  │
  ├─▶ [Indexing Phase]
  │     │
  │     ├─▶ Chunk documents (512 chars, 50 overlap)
  │     │     └─▶ ~150 chunks
  │     │
  │     ├─▶ Generate embeddings (all-MiniLM-L6-v2)
  │     │     └─▶ 384-dimensional vectors
  │     │
  │     ├─▶ Build FAISS index (IndexFlatIP)
  │     │     └─▶ data/iep_faiss.index
  │     │
  │     └─▶ Save metadata
  │           └─▶ data/iep_metadata.pkl
  │
  └─▶ [Runtime Phase]
        │
        ├─▶ User enters student info
        │
        ├─▶ Multi-query retrieval
        │     ├─▶ Occupation query
        │     ├─▶ Standards query
        │     └─▶ Examples query
        │
        ├─▶ Filter & combine results (top-15)
        │
        ├─▶ Format context for prompt
        │
        ├─▶ Build structured prompt
        │
        ├─▶ Call GPT-4 API
        │
        ├─▶ Parse structured output
        │
        └─▶ Display to user
              ├─▶ Show in UI
              └─▶ Download option
```

---

## Knowledge Base Structure

```
KNOWLEDGE BASE
│
├─── BLS OCCUPATIONAL DATA (60+ documents)
│    │
│    ├─── retail-sales-workers
│    │    ├─ Summary
│    │    ├─ Duties
│    │    ├─ Training/Education
│    │    └─ Requirements
│    │
│    ├─── delivery-truck-drivers
│    ├─── food-service
│    ├─── janitors
│    ├─── office-clerks
│    ├─── customer-service
│    ├─── cashiers
│    └─── warehouse-workers
│
├─── EDUCATIONAL STANDARDS (25+ documents)
│    │
│    ├─── Iowa 21st Century Skills
│    │    ├─ Employability Skills (6)
│    │    ├─ Communication Skills (4)
│    │    ├─ Critical Thinking (4)
│    │    └─ Self-Direction (4)
│    │
│    └─── IDEA 2004 Requirements
│         └─ Transition Planning (6)
│
└─── IEP EXAMPLES (7 documents)
     ├─ Employment Goals (2)
     ├─ Training Goals (1)
     ├─ Annual Objectives (2)
     └─ Short-term Objectives (2)
```

---

## Retrieval Strategy

```
USER QUERY: "Student interested in retail sales"
   │
   ├─▶ QUERY 1: "occupation duties requirements training for retail sales"
   │      │
   │      └─▶ FAISS Search (k=10)
   │            │
   │            └─▶ Filter: source == 'BLS_OOH'
   │                  └─▶ Top-5: BLS retail info
   │
   ├─▶ QUERY 2: "employability skills communication workplace for retail sales"
   │      │
   │      └─▶ FAISS Search (k=10)
   │            │
   │            └─▶ Filter: source in ['Iowa_Standards', 'IDEA_2004']
   │                  └─▶ Top-5: Relevant standards
   │
   └─▶ QUERY 3: "IEP transition goal retail sales employment training"
          │
          └─▶ FAISS Search (k=10)
                │
                └─▶ Filter: source == 'IEP_Examples'
                      └─▶ Top-5: Example goals

COMBINE & DEDUPLICATE
   │
   └─▶ CONTEXT (15 documents)
         ├─ Occupation info (5)
         ├─ Standards (5)
         └─ Examples (5)
```

---

## Prompt Structure

```
┌─────────────────────────────────────────────────────────┐
│                    SYSTEM PROMPT                         │
│  "You are an expert special education transition         │
│   planning specialist with deep knowledge of..."         │
└─────────────────────────────────────────────────────────┘
                           +
┌─────────────────────────────────────────────────────────┐
│                     USER PROMPT                          │
│                                                          │
│  SECTION 1: Student Information                         │
│  ┌────────────────────────────────────────────┐        │
│  │ Name: Clarence                              │        │
│  │ Age: 15, Grade: 10                         │        │
│  │ Interests: Retail sales                    │        │
│  │ Assessment: Strong in Enterprising         │        │
│  └────────────────────────────────────────────┘        │
│                                                          │
│  SECTION 2: Retrieved Context                           │
│  ┌────────────────────────────────────────────┐        │
│  │ === Career Information ===                 │        │
│  │ - Retail workers help customers...         │        │
│  │ - Duties include greeting customers...     │        │
│  │                                             │        │
│  │ === Relevant Standards ===                 │        │
│  │ - Communicate effectively...               │        │
│  │ - Demonstrate accountability...            │        │
│  │                                             │        │
│  │ === Example IEP Goals ===                  │        │
│  │ - After high school, [Student] will...    │        │
│  └────────────────────────────────────────────┘        │
│                                                          │
│  SECTION 3: Output Requirements                         │
│  ┌────────────────────────────────────────────┐        │
│  │ Generate:                                   │        │
│  │ 1. Measurable postsecondary goals (2+)     │        │
│  │ 2. Annual IEP objective (1)                │        │
│  │ 3. Short-term objectives (3-4)             │        │
│  │ 4. Standards alignment explanations        │        │
│  │                                             │        │
│  │ Requirements:                               │        │
│  │ • Be specific to Clarence                  │        │
│  │ • Use measurable criteria                  │        │
│  │ • Include timelines                        │        │
│  │ • Cite specific standards                  │        │
│  └────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
                      [ GPT-4 ]
                           │
                           ▼
                   [ Structured Output ]
```

---

## File Processing Pipeline

```
1. SCRAPING
   BLS Website → BeautifulSoup → JSON Cache
   
2. CHUNKING
   Text → RecursiveCharacterTextSplitter → Chunks (512 chars)
   
3. EMBEDDING
   Chunks → all-MiniLM-L6-v2 → Vectors (384-dim)
   
4. INDEXING
   Vectors → FAISS IndexFlatIP → Searchable Index
   
5. STORAGE
   Index → iep_faiss.index (binary)
   Metadata → iep_metadata.pkl (pickle)
```

---

## UI Component Layout

```
┌──────────────────────────────────────────────────────────────┐
│                    IEP GOAL GENERATOR                         │
│           RAG System for Transition Planning                  │
└──────────────────────────────────────────────────────────────┘

┌────────────────────┐  ┌──────────────────────────────────────┐
│   SIDEBAR          │  │         MAIN CONTENT AREA             │
│                    │  │                                       │
│ ┌────────────────┐ │  │ ┌──────────────┐ ┌─────────────────┐│
│ │ Student Info   │ │  │ │ Input        │ │ Retrieved       ││
│ │ • Name         │ │  │ │ Summary      │ │ Context         ││
│ │ • Age          │ │  │ │              │ │ Preview         ││
│ │ • Grade        │ │  │ │              │ │                 ││
│ │ • Interests    │ │  │ └──────────────┘ └─────────────────┘│
│ │ • Assessment   │ │  │                                       │
│ └────────────────┘ │  │ ┌─────────────────────────────────┐ │
│                    │  │ │  [ Generate IEP Goals Button ]   │ │
│ ┌────────────────┐ │  │ └─────────────────────────────────┘ │
│ │ Settings       │ │  │                                       │
│ │ • API Key      │ │  │ ┌─────────────────────────────────┐ │
│ │ • Model        │ │  │ │   GENERATED OUTPUT               │ │
│ │ • Temperature  │ │  │ │                                  │ │
│ └────────────────┘ │  │ │ 1. Postsecondary Goals          │ │
│                    │  │ │ 2. Annual Objective             │ │
│ [ Use Sample ]     │  │ │ 3. Short-term Objectives        │ │
│                    │  │ │ 4. Standards Alignment          │ │
│                    │  │ │                                  │ │
│                    │  │ │ [ Download Button ]             │ │
│                    │  │ └─────────────────────────────────┘ │
│                    │  │                                       │
│                    │  │ ┌─────────────────────────────────┐ │
│                    │  │ │   REFINEMENT                     │ │
│                    │  │ │   [Feedback TextBox]            │ │
│                    │  │ │   [ Refine Button ]             │ │
│                    │  │ └─────────────────────────────────┘ │
└────────────────────┘  └──────────────────────────────────────┘
```

---

## Setup & Execution Flow

```
┌──────────────┐
│ User runs    │
│ ./run.sh     │
└──────┬───────┘
       │
       ├─▶ Install dependencies
       │   └─▶ pip install -r requirements.txt
       │
       ├─▶ Test installation
       │   └─▶ python test_setup.py
       │
       ├─▶ Collect data
       │   └─▶ python src/data_collection.py
       │       ├─▶ Scrape BLS (5-10 min)
       │       └─▶ Save knowledge_base.pkl
       │
       ├─▶ Build index
       │   └─▶ python src/rag_pipeline.py
       │       ├─▶ Load embeddings model (30 sec)
       │       ├─▶ Generate embeddings
       │       └─▶ Save FAISS index
       │
       └─▶ Run application
           └─▶ streamlit run app.py
               └─▶ Opens http://localhost:8501
```

---

**These diagrams provide a visual representation of the system architecture, data flow, and component interactions.
