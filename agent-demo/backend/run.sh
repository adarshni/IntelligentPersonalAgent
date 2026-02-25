#!/bin/bash

# Agent Demo Backend Startup Script

echo "=========================================="
echo "  Intelligent Personal Agent - Backend   "
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo "Please copy .env.example to .env and configure your Azure OpenAI settings."
    echo ""
    cp .env.example .env
    echo "Created .env from .env.example. Please edit it with your credentials."
fi

# Run the application
echo ""
echo "Starting the backend server..."
echo "API will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
