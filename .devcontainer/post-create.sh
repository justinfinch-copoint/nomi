#!/bin/bash

# Post-create script for dev container setup
echo "Running post-create setup..."

# Install backend dependencies
if [ -f "nomi-backend/requirements.txt" ]; then
    echo "📦 Installing backend Python dependencies..."
    pip install -r nomi-backend/requirements.txt
else
    echo "⚠️  nomi-backend/requirements.txt not found, skipping backend install"
fi

# Install frontend dependencies
if [ -f "nomi-frontend/package.json" ]; then
    echo "📦 Installing frontend Node dependencies..."
    cd nomi-frontend
    npm install
    cd ..
else
    echo "⚠️  nomi-frontend/package.json not found, skipping frontend install"
fi

# Install Claude Code globally
echo "📦 Installing Claude Code..."
npm install -g @anthropic-ai/claude-code

echo "✅ Post-create setup complete!"
