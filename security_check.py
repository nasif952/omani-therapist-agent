#!/usr/bin/env python3
"""
Security Check Script for Omani Therapist AI
============================================

This script scans the codebase for potential security issues before GitHub upload.
It checks for:
- Exposed API keys
- Credentials
- Personal information
- Session data
"""

import os
import re
import sys
from pathlib import Path

# Patterns to detect sensitive information
SENSITIVE_PATTERNS = {
    'azure_key': r'AM1K[A-Za-z0-9]{59}',
    'openai_key': r'sk-proj-[A-Za-z0-9\-_]{100,}',
    'anthropic_key': r'sk-ant-api03-[A-Za-z0-9\-_]{90,}',
    'generic_api_key': r'["\']?[A-Za-z0-9]{32,}["\']?',
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'phone': r'\b\d{3}-\d{3}-\d{4}\b|\b\d{10}\b',
}

# File extensions to check
CHECK_EXTENSIONS = {'.py', '.md', '.txt', '.json', '.yml', '.yaml', '.env', '.ipynb'}

# Files and directories to skip
SKIP_PATTERNS = {
    '__pycache__',
    '.git',
    'node_modules',
    '.vscode',
    '.idea',
    'venv',
    'env',
    '.env',
    'omani_tts_samples',
    'therapy_session_',
}

def should_skip_file(file_path):
    """Check if file should be skipped"""
    path_str = str(file_path)
    
    # Skip if any skip pattern is in the path
    for pattern in SKIP_PATTERNS:
        if pattern in path_str:
            return True
    
    # Skip if extension is not in check list
    if file_path.suffix not in CHECK_EXTENSIONS:
        return True
    
    return False

def scan_file_for_sensitive_data(file_path):
    """Scan a single file for sensitive information"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        for pattern_name, pattern in SENSITIVE_PATTERNS.items():
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # Skip if it's clearly a placeholder
                matched_text = match.group(0)
                if any(placeholder in matched_text.lower() for placeholder in [
                    'your_', 'placeholder', 'example', 'template', 'xxx', '123'
                ]):
                    continue
                
                # Find line number
                line_num = content[:match.start()].count('\n') + 1
                issues.append({
                    'file': file_path,
                    'line': line_num,
                    'type': pattern_name,
                    'match': matched_text[:50] + '...' if len(matched_text) > 50 else matched_text
                })
    
    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}")
    
    return issues

def scan_directory(directory):
    """Scan entire directory for sensitive information"""
    all_issues = []
    files_scanned = 0
    
    print(f"🔍 Scanning directory: {directory}")
    print("-" * 50)
    
    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        dirs[:] = [d for d in dirs if not any(skip in d for skip in SKIP_PATTERNS)]
        
        for file in files:
            file_path = Path(root) / file
            
            if should_skip_file(file_path):
                continue
            
            files_scanned += 1
            issues = scan_file_for_sensitive_data(file_path)
            all_issues.extend(issues)
            
            if issues:
                print(f"🚨 {file_path}")
                for issue in issues:
                    print(f"   Line {issue['line']}: {issue['type']} - {issue['match']}")
            else:
                print(f"✅ {file_path}")
    
    print(f"\n📊 Scan Complete:")
    print(f"   Files scanned: {files_scanned}")
    print(f"   Issues found: {len(all_issues)}")
    
    return all_issues

def check_gitignore():
    """Check if .gitignore is properly configured"""
    gitignore_path = Path('.gitignore')
    
    if not gitignore_path.exists():
        print("❌ No .gitignore file found!")
        return False
    
    with open(gitignore_path, 'r') as f:
        gitignore_content = f.read()
    
    required_patterns = ['.env', '*.env', 'therapy_session_', '*session*.txt', '__pycache__']
    missing_patterns = []
    
    for pattern in required_patterns:
        if pattern not in gitignore_content:
            missing_patterns.append(pattern)
    
    if missing_patterns:
        print(f"⚠️  .gitignore missing patterns: {missing_patterns}")
        return False
    
    print("✅ .gitignore properly configured")
    return True

def main():
    """Main security check function"""
    print("🔒 SECURITY CHECK FOR GITHUB UPLOAD")
    print("=" * 50)
    
    # Check current directory
    current_dir = Path('.')
    
    # 1. Check .gitignore
    print("\n1. Checking .gitignore configuration...")
    gitignore_ok = check_gitignore()
    
    # 2. Scan for sensitive data
    print("\n2. Scanning for sensitive information...")
    issues = scan_directory(current_dir)
    
    # 3. Check for .env files
    print("\n3. Checking for .env files...")
    env_files = list(current_dir.rglob('*.env*'))
    if env_files:
        print("🚨 Found .env files:")
        for env_file in env_files:
            print(f"   - {env_file}")
    else:
        print("✅ No .env files found")
    
    # 4. Check for session files
    print("\n4. Checking for session files...")
    session_files = list(current_dir.rglob('*session*.txt'))
    if session_files:
        print("🚨 Found session files:")
        for session_file in session_files:
            print(f"   - {session_file}")
    else:
        print("✅ No session files found")
    
    # Final verdict
    print("\n" + "=" * 50)
    print("🏁 SECURITY CHECK RESULTS")
    print("=" * 50)
    
    if issues or env_files or session_files or not gitignore_ok:
        print("❌ SECURITY ISSUES FOUND!")
        print("   Fix these issues before uploading to GitHub:")
        if issues:
            print(f"   - {len(issues)} sensitive data patterns found")
        if env_files:
            print(f"   - {len(env_files)} .env files need to be removed/ignored")
        if session_files:
            print(f"   - {len(session_files)} session files need to be removed")
        if not gitignore_ok:
            print("   - .gitignore needs to be fixed")
        return False
    else:
        print("✅ SECURITY CHECK PASSED!")
        print("   Safe to upload to GitHub")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 