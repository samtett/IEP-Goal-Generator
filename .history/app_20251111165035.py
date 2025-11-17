"""
Streamlit User Interface for IEP Goal Generation System
"""

import streamlit as st
import os
import sys
import pickle
from typing import Dict

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.rag_pipeline import EmbeddingManager, VectorStore, ContextRetriever
from src.goal_generator import GoalGenerator, GoalParser


# Page configuration
st.set_page_config(
    page_title="IEP Goal Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource
def load_rag_system():
    """Load and cache the RAG system components"""
    try:
        embedding_manager = EmbeddingManager()
        vector_store = VectorStore(embedding_manager)
        
        # Try to load existing index
        if os.path.exists('data/iep_faiss.index'):
            vector_store.load()
        else:
            st.error("Vector index not found. Please run data collection first.")
            return None, None
        
        retriever = ContextRetriever(vector_store)
        return retriever, embedding_manager
    except Exception as e:
        st.error(f"Error loading RAG system: {str(e)}")
        return None, None


def main():
    """Main application"""
    
    # Header
    st.title("🎓 IEP Transition Goal Generator")
    st.markdown("""
    *Retrieval-Augmented Generation System for Special Education Transition Planning*
    
    This tool helps generate IDEA-compliant IEP transition goals aligned with industry 
    standards and educational frameworks.
    """)
    
    # Sidebar for student information
    st.sidebar.header("Student Information")
    
    # Check for sample data button
    use_sample = st.sidebar.checkbox("Use Sample Data (Clarence)")
    
    if use_sample:
        student_name = "Clarence"
        student_age = 15
        student_grade = "10"
        student_interests = "Retail sales, working at Walmart"
        student_assessment = "O*Net Interest Profiler - Strong in Enterprising activities. Career suggestions include retail salesperson and driver/sales worker."
        student_notes = "Prefers hands-on learning over academic instruction. Expressed interest in working at Walmart during 'Vision for the Future' interview."
    else:
        student_name = st.sidebar.text_input("Student Name", placeholder="Enter student name")
        student_age = st.sidebar.number_input("Age", min_value=14, max_value=22, value=16)
        student_grade = st.sidebar.selectbox("Grade", ["9", "10", "11", "12", "Post-secondary"])
        student_interests = st.sidebar.text_area(
            "Career Interests",
            placeholder="E.g., retail sales, food service, warehouse work"
        )
        student_assessment = st.sidebar.text_area(
            "Assessment Results",
            placeholder="E.g., O*Net Interest Profiler results, career assessments"
        )
        student_notes = st.sidebar.text_area(
            "Additional Notes (Optional)",
            placeholder="Any additional information about the student"
        )
    
    # API Key input
    st.sidebar.markdown("---")
    st.sidebar.header("⚙️ Settings")
    
    api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key. Get one at https://platform.openai.com/api-keys"
    )
    
    if not api_key:
        # Try to load from environment
        api_key = os.getenv('OPENAI_API_KEY')
    
    model_choice = st.sidebar.selectbox(
        "Model",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o-mini"],
        index=0,  # Default to gpt-3.5-turbo (available to all users)
        help="gpt-3.5-turbo is available to all users. GPT-4 models require special access and higher billing limits."
    )
    
    temperature = st.sidebar.slider(
        "Creativity (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more creative, lower values more focused"
    )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📋 Input Summary")
        
        if student_name:
            st.markdown(f"**Name:** {student_name}")
            st.markdown(f"**Age:** {student_age}")
            st.markdown(f"**Grade:** {student_grade}")
            st.markdown(f"**Interests:** {student_interests}")
            st.markdown(f"**Assessment:** {student_assessment}")
            if student_notes:
                st.markdown(f"**Notes:** {student_notes}")
        else:
            st.info("Please enter student information in the sidebar.")
    
    with col2:
        st.header("🔍 Retrieved Context")
        
        if student_interests and st.button("Preview Retrieved Context", type="secondary"):
            with st.spinner("Retrieving relevant information..."):
                retriever, _ = load_rag_system()
                
                if retriever:
                    student_info = {
                        'name': student_name,
                        'age': student_age,
                        'grade': student_grade,
                        'interests': student_interests,
                        'assessment': student_assessment,
                        'notes': student_notes
                    }
                    
                    results = retriever.retrieve_for_student(student_info)
                    
                    with st.expander("📊 Occupation Information", expanded=True):
                        for doc in results['occupation_info'][:2]:
                            st.markdown(f"- {doc['chunk_text'][:200]}...")
                    
                    with st.expander("📚 Educational Standards"):
                        for doc in results['standards'][:2]:
                            st.markdown(f"- {doc['chunk_text'][:200]}...")
                    
                    with st.expander("📝 Example Goals"):
                        for doc in results['examples'][:2]:
                            st.markdown(f"- {doc['chunk_text'][:200]}...")
    
    # Generate button
    st.markdown("---")
    
    if st.button("✨ Generate IEP Goals", type="primary", use_container_width=True):
        # Validation
        if not student_name or not student_interests:
            st.error("Please provide at least student name and career interests.")
            return
        
        if not api_key:
            st.error("Please provide an OpenAI API key in the sidebar or set OPENAI_API_KEY environment variable.")
            return
        
        # Load RAG system
        with st.spinner("Loading knowledge base..."):
            retriever, _ = load_rag_system()
            
            if not retriever:
                st.error("Failed to load RAG system. Please ensure data collection has been run.")
                return
        
        # Retrieve context
        with st.spinner("Retrieving relevant information..."):
            student_info = {
                'name': student_name,
                'age': student_age,
                'grade': student_grade,
                'interests': student_interests,
                'assessment': student_assessment,
                'notes': student_notes
            }
            
            results = retriever.retrieve_for_student(student_info)
            context = retriever.format_context_for_prompt(results)
        
        # Generate goals
        with st.spinner(f"Generating goals using {model_choice}... (this may take 30-60 seconds)"):
            try:
                generator = GoalGenerator(api_key=api_key, model=model_choice)
                result = generator.generate_goals(
                    student_info,
                    context,
                    temperature=temperature
                )
                
                if result['success']:
                    st.success("✅ Goals generated successfully!")
                    
                    # Display generated goals
                    st.markdown("---")
                    st.header("📄 Generated IEP Transition Goals")
                    
                    # Parse and display structured output
                    parsed = GoalParser.parse_goals(result['goals'])
                    
                    # Postsecondary Goals
                    st.subheader("1️⃣ Measurable Postsecondary Goals")
                    if parsed['postsecondary_goals']:
                        for i, goal in enumerate(parsed['postsecondary_goals'], 1):
                            st.markdown(f"**Goal {i}:**")
                            st.info(goal)
                    else:
                        st.markdown(result['goals'].split('ANNUAL')[0] if 'ANNUAL' in result['goals'] else result['goals'][:500])
                    
                    # Annual Objective
                    st.subheader("2️⃣ Annual IEP Objective")
                    if parsed['annual_objective']:
                        st.info(parsed['annual_objective'])
                    
                    # Short-term Objectives
                    st.subheader("3️⃣ Short-Term Objectives")
                    if parsed['short_term_objectives']:
                        for i, obj in enumerate(parsed['short_term_objectives'], 1):
                            st.markdown(f"**Objective {i}:**")
                            st.info(obj)
                    
                    # Standards Alignment
                    st.subheader("4️⃣ Standards Alignment")
                    if parsed['standards_alignment']:
                        st.info(parsed['standards_alignment'])
                    
                    # Full output in expander
                    with st.expander("📋 View Full Generated Output"):
                        st.markdown(result['goals'])
                    
                    # Download option
                    st.download_button(
                        label="📥 Download Goals as Text",
                        data=result['goals'],
                        file_name=f"IEP_Goals_{student_name.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                    
                    # Save to session state for refinement
                    st.session_state['last_generated'] = result['goals']
                    st.session_state['student_info'] = student_info
                    
                else:
                    st.error(f"Error generating goals: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Please check your API key and try again.")
    
    # Refinement section
    if 'last_generated' in st.session_state:
        st.markdown("---")
        st.header("🔄 Refine Goals")
        
        feedback = st.text_area(
            "Provide feedback for refinement:",
            placeholder="E.g., Make the goals more specific, adjust the timeline, focus more on communication skills"
        )
        
        if st.button("Refine Goals") and feedback:
            if not api_key:
                st.error("Please provide an OpenAI API key.")
            else:
                with st.spinner("Refining goals..."):
                    try:
                        generator = GoalGenerator(api_key=api_key, model=model_choice)
                        result = generator.refine_goals(
                            st.session_state['last_generated'],
                            feedback,
                            temperature=temperature
                        )
                        
                        if result['success']:
                            st.success(" Goals refined successfully!")
                            st.markdown(result['goals'])
                            
                            # Update session state
                            st.session_state['last_generated'] = result['goals']
                        else:
                            st.error(f"Error: {result.get('error', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <small>
        Built with ❤️ for Special Education Professionals | 
        Powered by RAG & OpenAI | 
        Compliant with IDEA 2004
        </small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
