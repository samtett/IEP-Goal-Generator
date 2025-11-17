"""
Alternative LLM Providers for IEP Goal Generation
Free and open-source options instead of OpenAI
"""

import os
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()


# ============================================================================
# OPTION 1: Ollama (Local, FREE, No API Key Required)
# ============================================================================
"""
Ollama runs models locally on your machine - completely free and private!

Installation:
1. Install Ollama: https://ollama.ai/
2. Pull a model: ollama pull llama3
3. pip install ollama

Models available:
- llama3 (8B, 70B) - Meta's Llama 3
- mistral - Mistral 7B
- codellama - Code-focused
- phi3 - Microsoft's Phi-3
"""

class OllamaGenerator:
    """Generate IEP goals using Ollama (local, free)"""
    
    def __init__(self, model: str = "llama3"):
        try:
            import ollama
            self.client = ollama
            self.model = model
        except ImportError:
            raise ImportError("Install ollama: pip install ollama")
    
    def generate_goals(self, student_info: Dict, context: str, 
                      temperature: float = 0.7) -> Dict:
        """Generate goals using Ollama"""
        
        system_prompt = """You are an expert in special education transition planning."""
        
        user_prompt = f"""Generate IEP transition goals for:
Student: {student_info.get('name')}, Age: {student_info.get('age')}
Interests: {student_info.get('interests')}

Context: {context}

Generate:
1. Postsecondary employment goal
2. Postsecondary training goal
3. Annual IEP objective
4. 3 short-term objectives
"""
        
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                options={'temperature': temperature}
            )
            
            return {
                'goals': response['message']['content'],
                'model': self.model,
                'success': True,
                'cost': 0.0  # FREE!
            }
        except Exception as e:
            return {'goals': None, 'error': str(e), 'success': False}


# ============================================================================
# OPTION 2: Groq (Cloud, FREE with API Key)
# ============================================================================
"""
Groq offers FREE API access with fast inference!

Setup:
1. Get free API key: https://console.groq.com/
2. pip install groq
3. Set GROQ_API_KEY in .env

Models available (all FREE):
- llama3-70b-8192 - Llama 3 70B
- llama3-8b-8192 - Llama 3 8B
- mixtral-8x7b-32768 - Mixtral
"""

class GroqGenerator:
    """Generate IEP goals using Groq (cloud, free)"""
    
    def __init__(self, api_key: Optional[str] = None, 
                 model: str = "llama3-70b-8192"):
        try:
            from groq import Groq
            self.api_key = api_key or os.getenv('GROQ_API_KEY')
            if not self.api_key:
                raise ValueError("Set GROQ_API_KEY in .env or pass as parameter")
            
            self.client = Groq(api_key=self.api_key)
            self.model = model
        except ImportError:
            raise ImportError("Install groq: pip install groq")
    
    def generate_goals(self, student_info: Dict, context: str,
                      temperature: float = 0.7) -> Dict:
        """Generate goals using Groq"""
        
        system_prompt = """You are an expert in special education transition planning."""
        
        user_prompt = f"""Generate IEP transition goals for:
Student: {student_info.get('name')}, Age: {student_info.get('age')}
Interests: {student_info.get('interests')}

Context: {context}

Generate:
1. Postsecondary employment goal
2. Postsecondary training goal  
3. Annual IEP objective
4. 3 short-term objectives
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=2000
            )
            
            return {
                'goals': response.choices[0].message.content,
                'model': self.model,
                'success': True,
                'cost': 0.0  # FREE!
            }
        except Exception as e:
            return {'goals': None, 'error': str(e), 'success': False}


# ============================================================================
# OPTION 3: Hugging Face (Local or Cloud, FREE)
# ============================================================================
"""
Use Hugging Face models locally or via their free inference API

Setup:
1. pip install transformers torch
2. For cloud: get free API key from https://huggingface.co/settings/tokens
3. Set HF_API_KEY in .env (optional)

Models available:
- meta-llama/Llama-3-8B-Instruct
- mistralai/Mistral-7B-Instruct-v0.2
- google/gemma-7b-it
"""

class HuggingFaceGenerator:
    """Generate IEP goals using Hugging Face models"""
    
    def __init__(self, model: str = "mistralai/Mistral-7B-Instruct-v0.2",
                 use_local: bool = False):
        self.model = model
        self.use_local = use_local
        
        if use_local:
            # Load model locally (requires GPU for best performance)
            try:
                from transformers import AutoTokenizer, AutoModelForCausalLM
                import torch
                
                self.tokenizer = AutoTokenizer.from_pretrained(model)
                self.model_obj = AutoModelForCausalLM.from_pretrained(
                    model,
                    torch_dtype=torch.float16,
                    device_map="auto"
                )
            except ImportError:
                raise ImportError("Install: pip install transformers torch")
        else:
            # Use Hugging Face Inference API (free tier available)
            try:
                from huggingface_hub import InferenceClient
                api_key = os.getenv('HF_API_KEY')
                self.client = InferenceClient(token=api_key)
            except ImportError:
                raise ImportError("Install: pip install huggingface_hub")
    
    def generate_goals(self, student_info: Dict, context: str,
                      temperature: float = 0.7) -> Dict:
        """Generate goals using Hugging Face"""
        
        prompt = f"""You are an expert in special education transition planning.

Generate IEP transition goals for:
Student: {student_info.get('name')}, Age: {student_info.get('age')}
Interests: {student_info.get('interests')}

Context: {context}

Generate:
1. Postsecondary employment goal
2. Postsecondary training goal
3. Annual IEP objective  
4. 3 short-term objectives
"""
        
        try:
            if self.use_local:
                inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
                outputs = self.model_obj.generate(
                    **inputs,
                    max_new_tokens=2000,
                    temperature=temperature
                )
                text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            else:
                text = self.client.text_generation(
                    prompt,
                    model=self.model,
                    max_new_tokens=2000,
                    temperature=temperature
                )
            
            return {
                'goals': text,
                'model': self.model,
                'success': True,
                'cost': 0.0  # FREE!
            }
        except Exception as e:
            return {'goals': None, 'error': str(e), 'success': False}


# ============================================================================
# OPTION 4: Anthropic Claude (Paid, but competitive pricing)
# ============================================================================
"""
Anthropic Claude - Alternative to OpenAI, often better for long contexts

Setup:
1. Get API key: https://console.anthropic.com/
2. pip install anthropic
3. Set ANTHROPIC_API_KEY in .env

Models:
- claude-3-opus-20240229 ($15/$75 per 1M tokens)
- claude-3-sonnet-20240229 ($3/$15 per 1M tokens)
- claude-3-haiku-20240307 ($0.25/$1.25 per 1M tokens)
"""

class ClaudeGenerator:
    """Generate IEP goals using Anthropic Claude"""
    
    def __init__(self, api_key: Optional[str] = None,
                 model: str = "claude-3-sonnet-20240229"):
        try:
            from anthropic import Anthropic
            self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
            if not self.api_key:
                raise ValueError("Set ANTHROPIC_API_KEY")
            
            self.client = Anthropic(api_key=self.api_key)
            self.model = model
        except ImportError:
            raise ImportError("Install: pip install anthropic")
    
    def generate_goals(self, student_info: Dict, context: str,
                      temperature: float = 0.7) -> Dict:
        """Generate goals using Claude"""
        
        prompt = f"""Generate IEP transition goals for:
Student: {student_info.get('name')}, Age: {student_info.get('age')}
Interests: {student_info.get('interests')}

Context: {context}

Generate:
1. Postsecondary employment goal
2. Postsecondary training goal
3. Annual IEP objective
4. 3 short-term objectives
"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=temperature,
                system="You are an expert in special education transition planning.",
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                'goals': response.content[0].text,
                'model': self.model,
                'success': True
            }
        except Exception as e:
            return {'goals': None, 'error': str(e), 'success': False}


# ============================================================================
# COMPARISON SUMMARY
# ============================================================================
"""
BEST FREE OPTIONS:

1. **Ollama** (RECOMMENDED FOR STUDENTS/PRIVACY)
   ✅ Completely FREE
   ✅ Runs locally (100% private)
   ✅ No API key needed
   ✅ Good quality with llama3
   ❌ Requires ~4-8GB VRAM
   ❌ Slower on CPU

2. **Groq**
   ✅ FREE API
   ✅ Very fast inference
   ✅ Good model quality (Llama 3 70B)
   ✅ Easy to use
   ❌ Requires internet
   ❌ Rate limits on free tier

3. **Hugging Face Inference API**
   ✅ FREE tier available
   ✅ Many models to choose from
   ✅ Can run locally too
   ❌ Free tier has limits
   ❌ May be slower

PAID BUT CHEAPER THAN OPENAI:

4. **Anthropic Claude**
   ✅ Often better quality than GPT-4
   ✅ Cheaper than OpenAI for some models
   ✅ Better at long contexts
   ❌ Still requires payment

RECOMMENDED APPROACH:
- For development/testing: Use Ollama (free, local)
- For production: Use Groq (free, fast) or Claude (paid, best quality)
- For maximum privacy: Use Ollama or local Hugging Face
"""


if __name__ == "__main__":
    print("Alternative LLM Options for IEP Goal Generation")
    print("=" * 60)
    print("\n1. Ollama (Local, FREE)")
    print("   Install: https://ollama.ai/")
    print("   Usage: OllamaGenerator(model='llama3')")
    print("\n2. Groq (Cloud, FREE)")
    print("   Get key: https://console.groq.com/")
    print("   Usage: GroqGenerator(api_key='your-key')")
    print("\n3. Hugging Face (Local/Cloud, FREE)")
    print("   Get key: https://huggingface.co/settings/tokens")
    print("   Usage: HuggingFaceGenerator(use_local=False)")
    print("\n4. Anthropic Claude (Cloud, Paid)")
    print("   Get key: https://console.anthropic.com/")
    print("   Usage: ClaudeGenerator(api_key='your-key')")
