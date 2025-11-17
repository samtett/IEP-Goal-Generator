# Quick Start Guide

## 🚀 Fast Setup (5 minutes)

### Step 1: Install Dependencies (1 min)

```bash
# Navigate to project directory
cd /home/samtett/Documents/NLP

# Install all required packages
pip install -r requirements.txt
```

### Step 2: Set Up API Key (1 min)

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Get your API key**: https://platform.openai.com/api-keys

### Step 3: Test Installation (1 min)

```bash
python test_setup.py
```

This verifies all packages are installed correctly.

### Step 4: Collect Data (2 min)

```bash
# Collect BLS occupation data and build knowledge base
python src/data_collection.py

# Build FAISS vector index
python src/rag_pipeline.py
```

### Step 5: Run the App! (<1 min)

```bash
streamlit run app.py
```

Opens in browser at http://localhost:8501

---

## ✨ Using the App (First Time)

1. **Check "Use Sample Data (Clarence)"** in sidebar
   - This loads the example student profile

2. **Enter Your OpenAI API Key** (if not in `.env`)
   - In Settings section of sidebar

3. **Click "Generate IEP Goals"**
   - Wait 30-60 seconds
   - Review generated goals

4. **Download or Refine**
   - Download as text file, or
   - Provide feedback to refine

---

## 📋 Sample Student Profile

The app includes a ready-to-use example:

- **Name**: Clarence
- **Age**: 15, Grade 10
- **Interests**: Retail sales, Walmart
- **Assessment**: Strong in Enterprising (O*Net)

Expected output includes:
- Employment goal (retail position)
- Training goal (on-the-job training)
- Annual objective (customer service skills)
- 3-4 short-term objectives
- Standards alignment

---

## 🔧 Troubleshooting

### "Import could not be resolved" errors
```bash
pip install -r requirements.txt
```

### "Vector index not found"
```bash
python src/data_collection.py
python src/rag_pipeline.py
```

### "OpenAI API key error"
- Check `.env` file has correct key
- Or enter key directly in app sidebar

### "FAISS error on Apple Silicon"
```bash
# Use conda instead
conda install -c pytorch faiss-cpu
```

---

## 💡 Tips

- **First generation**: Use sample data to test
- **Best quality**: Use GPT-4 (more expensive but better)
- **Faster/cheaper**: Use GPT-3.5-turbo
- **Refinement**: Provide specific feedback (e.g., "make more specific", "add timeline")
- **Privacy**: Student data is only sent to OpenAI, not stored locally

---

## 📊 What It Does

1. **Retrieves** relevant career info from BLS database
2. **Finds** matching educational standards
3. **Uses** example IEP goals as reference
4. **Generates** custom goals using GPT-4
5. **Aligns** with IDEA 2004 requirements

---

## 🎯 Next Steps

After your first successful generation:

1. Try with custom student data
2. Experiment with different career interests
3. Refine goals based on feedback
4. Download and use in actual IEP documents
5. Customize for your state's standards

---

## 📞 Need Help?

1. Run `python test_setup.py` to diagnose issues
2. Check README.md for detailed documentation
3. Verify all steps completed successfully
4. Ensure Python 3.8+ is installed

---

**Ready to go?** Run: `streamlit run app.py` 🚀
