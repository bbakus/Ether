#!/bin/bash

echo "Current directory: $(pwd)"
echo "Listing root contents:"
ls -la

echo "Checking if client directory exists..."
if [ -d "client" ]; then
    echo "Client directory found!"
    echo "Listing client contents:"
    ls -la client/
    
    echo "Installing npm dependencies in client directory..."
    cd client && npm install
    
    echo "Building React app..."
    npm run build
    
    echo "Build completed! Listing build directory:"
    ls -la build/
    
    echo "Moving back to root and checking final build output:"
    cd ..
    ls -la client/build/
else
    echo "ERROR: client directory not found!"
    echo "Available directories:"
    find . -type d -name "*client*" 2>/dev/null || echo "No client directories found"
fi 