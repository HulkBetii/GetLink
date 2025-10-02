#!/bin/bash

# Course Link Getter - Push to GitHub Script
echo "🚀 Pushing Course Link Getter to GitHub..."

# Navigate to project directory
cd /Users/sangspm/Documents/GetLink

# Check if we're in the right directory
echo "📁 Current directory: $(pwd)"
echo "📋 Files in directory:"
ls -la

# Initialize git repository
echo "🔧 Initializing git repository..."
git init

# Add all files
echo "📦 Adding all files to git..."
git add .

# Check git status
echo "📊 Git status:"
git status

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Course Link Getter

Complete desktop application with:
- PyQt5 desktop UI with advanced filtering
- Web-based interface using Python HTTP server  
- Interactive CLI for quick access
- Comprehensive pytest test suite (15 tests, <2s runtime)
- Settings persistence with cross-platform support
- CSV export and clipboard integration
- GitHub Actions CI/CD workflows
- 26+ courses across 3 categories with real-time search

Features:
✅ Real-time filtering by category, subcategory, and text
✅ Get Link functionality with clipboard integration
✅ Export to CSV with specified columns
✅ Settings persistence and restoration
✅ Comprehensive test coverage with CI-friendly execution
✅ Cross-platform support (macOS, Windows, Linux)"

# Add remote origin
echo "🔗 Adding remote origin..."
git remote add origin https://github.com/HulkBetii/GetLink.git

# Set main branch
echo "🌿 Setting main branch..."
git branch -M main

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push -u origin main

echo "✅ Course Link Getter successfully pushed to GitHub!"
echo "🔗 Repository: https://github.com/HulkBetii/GetLink.git"
echo "📋 Branch: main"
