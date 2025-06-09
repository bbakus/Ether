#!/bin/bash

# Navigate to server directory
cd server

# Install Python dependencies
pip install -r requirements.txt

# Create and seed database
python create_db.py
python seed.py

echo "Backend build completed successfully!" 