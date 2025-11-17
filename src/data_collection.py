"""
Data Collection Module for IEP RAG System
Handles scraping BLS Occupational Outlook Handbook and loading educational standards
"""

import os
import json
import pickle
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import time


class BLSDataCollector:
    """Scrapes and processes data from Bureau of Labor Statistics Occupational Outlook Handbook"""
    
    BASE_URL = "https://www.bls.gov/ooh"
    
    # Key occupations relevant to special education transition planning
    TARGET_OCCUPATIONS = {
        'retail-sales-workers': 'sales/retail-sales-workers.htm',
        'delivery-truck-drivers': 'transportation/delivery-truck-drivers-and-driver-sales-workers.htm',
        'food-service': 'food-preparation-and-serving/food-and-beverage-serving-and-related-workers.htm',
        'janitors': 'building-and-grounds-cleaning/janitors-and-building-cleaners.htm',
        'office-clerks': 'office-and-administrative-support/general-office-clerks.htm',
        'customer-service': 'office-and-administrative-support/customer-service-representatives.htm',
        'cashiers': 'sales/cashiers.htm',
        'warehouse-workers': 'transportation/material-moving-occupations.htm',
    }
    
    def __init__(self, cache_dir: str = "data/scraped"):
        """Initialize the BLS data collector
        
        Args:
            cache_dir: Directory to cache scraped data
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def scrape_occupation(self, occupation_name: str, url_path: str) -> Dict[str, str]:
        """Scrape detailed information for a specific occupation
        
        Args:
            occupation_name: Name identifier for the occupation
            url_path: URL path relative to BLS OOH base
            
        Returns:
            Dictionary containing occupation details
        """
        cache_file = os.path.join(self.cache_dir, f"{occupation_name}.json")
        
        # Check cache first
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)
        
        url = f"{self.BASE_URL}/{url_path}"
        print(f"Scraping {occupation_name} from {url}")
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract key sections
            data = {
                'occupation': occupation_name,
                'url': url,
                'summary': self._extract_section(soup, 'what-they-do'),
                'duties': self._extract_section(soup, 'duties'),
                'work_environment': self._extract_section(soup, 'work-environment'),
                'education_training': self._extract_section(soup, 'how-to-become-one'),
                'requirements': self._extract_section(soup, 'requirements'),
                'pay': self._extract_section(soup, 'pay'),
                'job_outlook': self._extract_section(soup, 'job-outlook'),
            }
            
            # Cache the result
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            time.sleep(1)  # Be respectful to the server
            return data
            
        except Exception as e:
            print(f"Error scraping {occupation_name}: {str(e)}")
            return {'occupation': occupation_name, 'error': str(e)}
    
    def _extract_section(self, soup: BeautifulSoup, section_id: str) -> str:
        """Extract text from a specific section of the page
        
        Args:
            soup: BeautifulSoup object of the page
            section_id: ID of the section to extract
            
        Returns:
            Cleaned text content
        """
        section = soup.find('div', id=section_id)
        if section:
            # Remove script and style elements
            for script in section(["script", "style"]):
                script.decompose()
            text = section.get_text(separator=' ', strip=True)
            return ' '.join(text.split())  # Normalize whitespace
        return ""
    
    def collect_all_occupations(self) -> List[Dict[str, str]]:
        """Scrape all target occupations
        
        Returns:
            List of occupation data dictionaries
        """
        all_data = []
        for name, path in self.TARGET_OCCUPATIONS.items():
            data = self.scrape_occupation(name, path)
            if 'error' not in data:
                all_data.append(data)
        return all_data


class EducationalStandardsLoader:
    """Loads and processes educational standards documents"""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize standards loader
        
        Args:
            data_dir: Directory containing standards files
        """
        self.data_dir = data_dir
    
    def load_iowa_standards(self) -> Dict[str, List[str]]:
        """Load Iowa 21st Century Skills standards
        
        Returns:
            Dictionary of standards organized by category
        """
        # These are key employability standards from Iowa's framework
        standards = {
            'employability_skills': [
                "Communicate and work productively with others, incorporating different perspectives and cross-cultural understanding, to increase innovation and the quality of work",
                "Adapt to various roles and responsibilities and work flexibly in climates of ambiguity and changing priorities",
                "Demonstrate initiative and entrepreneurial thinking by exploring new or innovative solutions",
                "Demonstrate productivity and accountability by meeting high expectations",
                "Show leadership by setting goals, resolving conflicts, and guiding others",
                "Demonstrate ethical behavior and respect for others",
            ],
            'communication_skills': [
                "Listen actively to decipher meaning, including knowledge, values, attitudes, and intentions",
                "Use communication for a range of purposes (e.g., to inform, instruct, motivate, and persuade)",
                "Use multiple media and technologies to communicate effectively",
                "Communicate effectively in diverse environments (including multilingual and multicultural)",
            ],
            'critical_thinking': [
                "Exercise sound reasoning in understanding and making complex choices",
                "Understand the interconnections among systems",
                "Identify and ask significant questions that clarify various points of view",
                "Frame, analyze, and solve problems",
            ],
            'self_direction': [
                "Monitor one's own learning and adapt strategies as needed",
                "Demonstrate initiative to advance skill levels toward professional level",
                "Set and meet high standards and goals for oneself and others",
                "Manage time and projects effectively",
            ],
        }
        return standards
    
    def load_idea_requirements(self) -> List[str]:
        """Load IDEA 2004 transition planning requirements
        
        Returns:
            List of key requirements
        """
        return [
            "Include appropriate measurable postsecondary goals based upon age-appropriate transition assessments related to training, education, employment, and, where appropriate, independent living skills",
            "Include the transition services (including courses of study) needed to assist the child in reaching those goals",
            "Goals must be updated annually, beginning not later than the first IEP to be in effect when the child turns 16",
            "Postsecondary goals must be measurable",
            "Transition assessments must be age-appropriate",
            "Goals should be based on student's strengths, preferences, and interests",
        ]
    
    def get_all_standards(self) -> Dict[str, any]:
        """Get all standards combined
        
        Returns:
            Dictionary with all standards data
        """
        return {
            'iowa_standards': self.load_iowa_standards(),
            'idea_requirements': self.load_idea_requirements(),
        }


class IEPExamplesLoader:
    """Loads sample IEP goals and objectives for reference"""
    
    @staticmethod
    def load_sample_goals() -> List[Dict[str, str]]:
        """Load sample IEP transition goals
        
        Returns:
            List of sample goal dictionaries
        """
        return [
            {
                'type': 'employment_goal',
                'text': "After high school, [Student] will obtain a full-time job at [Company] as a [Position].",
                'context': 'Postsecondary employment goal for retail',
            },
            {
                'type': 'training_goal',
                'text': "After high school, [Student] will complete on-the-job training provided by [Employer] and participate in employer-sponsored workshops.",
                'context': 'Postsecondary education/training goal',
            },
            {
                'type': 'annual_objective',
                'text': "In 36 weeks, [Student] will demonstrate effective workplace communication and customer service skills in role-play and community-based instruction settings by appropriately greeting customers, maintaining eye contact, listening actively, and responding to customer questions in 4 out of 5 observed opportunities.",
                'context': 'Annual IEP objective aligned with employability standards',
            },
            {
                'type': 'short_term_objective',
                'text': "Within 12 weeks, [Student] will practice appropriate workplace greetings with staff and peers in the classroom setting, using eye contact and clear speech in 8 out of 10 opportunities.",
                'context': 'Short-term objective building toward annual goal',
            },
            {
                'type': 'short_term_objective',
                'text': "Within 24 weeks, [Student] will demonstrate active listening skills by responding appropriately to supervisor instructions during community-based instruction in 4 out of 5 trials.",
                'context': 'Short-term objective for listening skills',
            },
            {
                'type': 'employment_goal',
                'text': "Upon completion of high school, [Student] will obtain competitive integrated employment in the food service industry working at least 20 hours per week.",
                'context': 'Postsecondary employment goal for food service',
            },
            {
                'type': 'annual_objective',
                'text': "By the end of the IEP period, [Student] will demonstrate job-seeking skills by completing online job applications, preparing a resume, and participating in mock interviews with 80% accuracy.",
                'context': 'Annual objective for job readiness',
            },
        ]


def build_knowledge_base() -> List[Dict[str, str]]:
    """Build complete knowledge base from all sources
    
    Returns:
        List of documents with text and metadata
    """
    documents = []
    
    # Collect BLS occupation data
    print("Collecting BLS occupation data...")
    bls_collector = BLSDataCollector()
    occupations = bls_collector.collect_all_occupations()
    
    for occ in occupations:
        # Add each section as a separate document for better retrieval
        if occ.get('summary'):
            documents.append({
                'text': f"Occupation: {occ['occupation']}\nSummary: {occ['summary']}",
                'source': 'BLS_OOH',
                'occupation': occ['occupation'],
                'section': 'summary'
            })
        if occ.get('duties'):
            documents.append({
                'text': f"Occupation: {occ['occupation']}\nDuties and Responsibilities: {occ['duties']}",
                'source': 'BLS_OOH',
                'occupation': occ['occupation'],
                'section': 'duties'
            })
        if occ.get('education_training'):
            documents.append({
                'text': f"Occupation: {occ['occupation']}\nEducation and Training Requirements: {occ['education_training']}",
                'source': 'BLS_OOH',
                'occupation': occ['occupation'],
                'section': 'training'
            })
    
    # Load educational standards
    print("Loading educational standards...")
    standards_loader = EducationalStandardsLoader()
    all_standards = standards_loader.get_all_standards()
    
    # Add Iowa standards
    for category, skills in all_standards['iowa_standards'].items():
        for skill in skills:
            documents.append({
                'text': f"Iowa 21st Century Skills - {category.replace('_', ' ').title()}: {skill}",
                'source': 'Iowa_Standards',
                'category': category,
                'section': 'standards'
            })
    
    # Add IDEA requirements
    for requirement in all_standards['idea_requirements']:
        documents.append({
            'text': f"IDEA 2004 Transition Requirement: {requirement}",
            'source': 'IDEA_2004',
            'section': 'requirements'
        })
    
    # Load sample IEP goals
    print("Loading sample IEP goals...")
    sample_goals = IEPExamplesLoader.load_sample_goals()
    for goal in sample_goals:
        documents.append({
            'text': f"Sample {goal['type'].replace('_', ' ').title()}: {goal['text']}\nContext: {goal['context']}",
            'source': 'IEP_Examples',
            'type': goal['type'],
            'section': 'examples'
        })
    
    print(f"Built knowledge base with {len(documents)} documents")
    return documents


if __name__ == "__main__":
    # Test the data collection
    docs = build_knowledge_base()
    
    # Save to pickle for later use
    with open('data/knowledge_base.pkl', 'wb') as f:
        pickle.dump(docs, f)
    
    print(f"\nSaved {len(docs)} documents to data/knowledge_base.pkl")
    print("\nSample documents:")
    for i, doc in enumerate(docs[:3]):
        print(f"\n{i+1}. Source: {doc['source']}")
        print(f"   Text: {doc['text'][:150]}...")
