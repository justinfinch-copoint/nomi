#!/bin/bash

# Post-create script for dev container setup
echo "Running post-create setup..."

echo "📦 Installing requirements..."
pip install -r requirements.txt

# Install Claude Code globally
echo "📦 Installing Claude Code..."
npm install -g @anthropic-ai/claude-code

echo "✅ Post-create setup complete!"
