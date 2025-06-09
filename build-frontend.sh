#!/bin/bash

echo "Current directory: $(pwd)"
echo "Listing root contents:"
ls -la

echo "Navigating to client directory..."
cd client

echo "Current directory after cd: $(pwd)"
echo "Listing client contents:"
ls -la

echo "Installing npm dependencies..."
npm install

echo "Building React app..."
npm run build

echo "Build completed! Listing build directory:"
ls -la build/ 