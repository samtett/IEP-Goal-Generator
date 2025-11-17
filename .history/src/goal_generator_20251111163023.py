"""
Prompt Engineering and Goal Generation Module
Handles LLM prompts and goal generation
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


class PromptBuilder:
    """Builds effective prompts for IEP goal generation"""
    
    SYSTEM_PROMPT = """You are an expert special education transition planning specialist with deep knowledge of:
- IDEA 2004 transition planning requirements
- Writing measurable postsecondary goals
- Developing appropriate IEP objectives and benchmarks
- Aligning goals with industry standards and educational frameworks
- Career pathways and occupational requirements

Your role is to generate high-quality, legally compliant IEP transition goals that are:
1. Measurable and specific
2. Based on student strengths, preferences, and interests
3. Aligned with relevant industry standards and educational frameworks
4. Appropriate for the student's age and grade level
5. Realistic and achievable"""
    
    @staticmethod
    def build_goal_generation_prompt(student_info: Dict[str, str], 
                                     context: str) -> str:
        """Build prompt for generating IEP goals
        
        Args:
            student_info: Dictionary with student information
            context: Retrieved context from RAG system
            
        Returns:
            Complete prompt string
        """
        prompt = f"""Generate comprehensive IEP transition goals for the following student:

STUDENT INFORMATION:
- Name: {student_info.get('name', 'Student')}
- Age: {student_info.get('age', 'Not specified')}
- Grade: {student_info.get('grade', 'Not specified')}
- Career Interests: {student_info.get('interests', 'Not specified')}
- Assessment Results: {student_info.get('assessment', 'Not specified')}
- Additional Notes: {student_info.get('notes', 'None')}

RELEVANT CONTEXT FROM KNOWLEDGE BASE:
{context}

REQUIRED OUTPUT:
Please generate the following components:

1. MEASURABLE POSTSECONDARY GOALS (at least 2):
   a) Employment Goal: A specific, measurable goal for competitive integrated employment
   b) Education/Training Goal: A specific goal for post-secondary education or training
   
2. ANNUAL IEP OBJECTIVE:
   - Create ONE comprehensive annual objective that aligns with the postsecondary goals
   - Must be measurable with clear criteria (e.g., "in 4 out of 5 opportunities")
   - Should incorporate workplace or career-relevant skills
   - Must align with educational standards (21st Century Skills, employability standards)

3. SHORT-TERM OBJECTIVES (3-4 objectives):
   - Create 3-4 short-term objectives that build toward the annual goal
   - Each should have a specific timeline (e.g., "within 12 weeks")
   - Include measurable criteria
   - Show progression from basic to more advanced skills

4. STANDARDS ALIGNMENT:
   - Explicitly explain how each goal aligns with:
     * Relevant occupational requirements (from BLS Occupational Outlook Handbook)
     * Iowa 21st Century Skills or similar employability standards
     * IDEA 2004 transition planning requirements
   - Cite specific standards when possible

FORMAT YOUR RESPONSE CLEARLY with headers for each section.
Make goals specific to {student_info.get('name', 'the student')} and their interest in {student_info.get('interests', 'their career field')}.
"""
        return prompt
    
    @staticmethod
    def build_refinement_prompt(original_goals: str, 
                               feedback: str) -> str:
        """Build prompt for refining generated goals
        
        Args:
            original_goals: Previously generated goals
            feedback: User feedback or refinement request
            
        Returns:
            Refinement prompt
        """
        prompt = f"""Please refine the following IEP transition goals based on the feedback provided.

ORIGINAL GOALS:
{original_goals}

FEEDBACK/REFINEMENT REQUEST:
{feedback}

Please provide the revised goals, maintaining the same structure and ensuring all requirements are met.
"""
        return prompt


class GoalGenerator:
    """Generates IEP goals using OpenAI API"""
    
    def __init__(self, api_key: Optional[str] = None, 
                 model: str = "gpt-4"):
        """Initialize goal generator
        
        Args:
            api_key: OpenAI API key (if not in environment)
            model: Model to use for generation
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model or os.getenv('OPENAI_MODEL', 'gpt-4')
        
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        openai.api_key = self.api_key
        self.prompt_builder = PromptBuilder()
    
    def generate_goals(self, student_info: Dict[str, str], 
                      context: str,
                      temperature: float = 0.7) -> Dict[str, str]:
        """Generate IEP goals for a student
        
        Args:
            student_info: Dictionary with student information
            context: Retrieved context from RAG system
            temperature: Sampling temperature for generation
            
        Returns:
            Dictionary with generated goals and metadata
        """
        print(f"Generating IEP goals for {student_info.get('name', 'student')}...")
        
        prompt = self.prompt_builder.build_goal_generation_prompt(
            student_info, context
        )
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.prompt_builder.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=2000
            )
            
            generated_text = response['choices'][0]['message']['content']
            
            return {
                'goals': generated_text,
                'student_name': student_info.get('name', 'Student'),
                'model': self.model,
                'prompt': prompt,
                'success': True
            }
            
        except Exception as e:
            print(f"Error generating goals: {str(e)}")
            return {
                'goals': None,
                'error': str(e),
                'success': False
            }
    
    def refine_goals(self, original_goals: str, 
                     feedback: str,
                     temperature: float = 0.7) -> Dict[str, str]:
        """Refine previously generated goals
        
        Args:
            original_goals: Original generated goals
            feedback: Refinement feedback
            temperature: Sampling temperature
            
        Returns:
            Dictionary with refined goals
        """
        print("Refining goals based on feedback...")
        
        prompt = self.prompt_builder.build_refinement_prompt(
            original_goals, feedback
        )
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.prompt_builder.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=2000
            )
            
            refined_text = response['choices'][0]['message']['content']
            
            return {
                'goals': refined_text,
                'success': True
            }
            
        except Exception as e:
            print(f"Error refining goals: {str(e)}")
            return {
                'goals': None,
                'error': str(e),
                'success': False
            }


class GoalParser:
    """Parses generated goals into structured format"""
    
    @staticmethod
    def parse_goals(generated_text: str) -> Dict[str, any]:
        """Parse generated goals into structured components
        
        Args:
            generated_text: Raw generated text from LLM
            
        Returns:
            Dictionary with parsed goal components
        """
        # Simple parsing based on section headers
        sections = {
            'postsecondary_goals': [],
            'annual_objective': '',
            'short_term_objectives': [],
            'standards_alignment': ''
        }
        
        lines = generated_text.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            
            # Detect section headers
            if 'POSTSECONDARY GOAL' in line.upper() or 'EMPLOYMENT GOAL' in line.upper():
                if current_section and current_content:
                    sections = GoalParser._save_section(sections, current_section, current_content)
                current_section = 'postsecondary_goals'
                current_content = []
            elif 'ANNUAL' in line.upper() and 'OBJECTIVE' in line.upper():
                if current_section and current_content:
                    sections = GoalParser._save_section(sections, current_section, current_content)
                current_section = 'annual_objective'
                current_content = []
            elif 'SHORT-TERM' in line.upper() or 'SHORT TERM' in line.upper():
                if current_section and current_content:
                    sections = GoalParser._save_section(sections, current_section, current_content)
                current_section = 'short_term_objectives'
                current_content = []
            elif 'STANDARDS ALIGNMENT' in line.upper() or 'ALIGNMENT' in line.upper():
                if current_section and current_content:
                    sections = GoalParser._save_section(sections, current_section, current_content)
                current_section = 'standards_alignment'
                current_content = []
            elif line and current_section:
                current_content.append(line)
        
        # Save the last section
        if current_section and current_content:
            sections = GoalParser._save_section(sections, current_section, current_content)
        
        return sections
    
    @staticmethod
    def _save_section(sections: Dict, section_name: str, content: List[str]) -> Dict:
        """Helper to save parsed section content"""
        text = '\n'.join(content)
        
        if section_name == 'postsecondary_goals':
            sections['postsecondary_goals'].append(text)
        elif section_name == 'short_term_objectives':
            sections['short_term_objectives'].append(text)
        else:
            sections[section_name] = text
        
        return sections


if __name__ == "__main__":
    # Test prompt building
    test_student = {
        'name': 'Clarence',
        'age': 15,
        'grade': '10',
        'interests': 'retail sales',
        'assessment': 'O*Net Interest Profiler - Strong in Enterprising activities'
    }
    
    test_context = """
=== Career Information ===
- Occupation: retail-sales-workers
  Duties: Retail sales workers help customers find products, process payments, and provide customer service.
  
=== Relevant Standards ===
- Iowa 21st Century Skills - Communication: Use communication for a range of purposes
- IDEA 2004: Include appropriate measurable postsecondary goals
    """
    
    builder = PromptBuilder()
    prompt = builder.build_goal_generation_prompt(test_student, test_context)
    
    print("Generated Prompt:")
    print("="*70)
    print(prompt)
    print("="*70)
    
    # Note: Actual generation requires valid API key
    print("\nTo test goal generation, ensure OPENAI_API_KEY is set in .env file")
