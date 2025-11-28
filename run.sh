#!/bin/bash

# IEP RAG System - Setup and Run Script

echo "=========================================="
echo "IEP RAG System - Setup Script"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo " Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo " Error: app.py not found. Please run this script from the project root directory."
    exit 1
fi

# Function to check if data exists
check_data() {
    if [ -f "data/iep_faiss.index" ] && [ -f "data/iep_metadata.pkl" ]; then
        return 0
    else
        return 1
    fi
}

# Menu
echo "What would you like to do?"
echo ""
echo "1) First-time setup (install dependencies + collect data)"
echo "2) Install dependencies only"
echo "3) Collect data and build index"
echo "4) Run the application"
echo "5) Test installation"
echo "6) Exit"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo ""
        echo "=========================================="
        echo "Running First-Time Setup"
        echo "=========================================="
        echo ""
        
        echo "Step 1/4: Installing dependencies..."
        pip3 install -r requirements.txt
        
        echo ""
        echo "Step 2/4: Testing installation..."
        python3 test_setup.py
        
        echo ""
        echo "Step 3/4: Collecting data from BLS..."
        python3 src/data_collection.py
        
        echo ""
        echo "Step 4/4: Building vector index..."
        python3 src/rag_pipeline.py
        
        echo ""
        echo " Setup complete!"
        echo ""
        read -p "Would you like to run the application now? (y/n): " run_app
        if [ "$run_app" = "y" ] || [ "$run_app" = "Y" ]; then
            echo ""
            echo "Starting application..."
            streamlit run app.py
        fi
        ;;
        
    2)
        echo ""
        echo "Installing dependencies..."
        pip3 install -r requirements.txt
        echo ""
        echo " Dependencies installed!"
        ;;
        
    3)
        echo ""
        echo "Collecting data from BLS..."
        python3 src/data_collection.py
        echo ""
        echo "Building vector index..."
        python3 src/rag_pipeline.py
        echo ""
        echo " Data collection complete!"
        ;;
        
    4)
        echo ""
        if check_data; then
            echo "Starting application..."
            echo "Opening in browser at http://localhost:8501"
            echo ""
            streamlit run app.py
        else
            echo " Data not found. Please run data collection first (option 3)."
            echo ""
            read -p "Would you like to collect data now? (y/n): " collect
            if [ "$collect" = "y" ] || [ "$collect" = "Y" ]; then
                python3 src/data_collection.py
                python3 src/rag_pipeline.py
                echo ""
                echo "Starting application..."
                streamlit run app.py
            fi
        fi
        ;;
        
    5)
        echo ""
        echo "Running installation tests..."
        python3 test_setup.py
        ;;
        
    6)
        echo "Goodbye!"
        exit 0
        ;;
        
    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac
