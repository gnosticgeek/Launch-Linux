#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Create main directories
mkdir -p bin lib roles playbooks tests docs .vscode

# Create initial files
touch README.md
touch .gitignore
touch bin/launch
touch lib/ascii.sh
touch roles/.gitkeep
touch playbooks/main.yml
touch tests/.gitkeep
touch docs/user_guide.md
touch .vscode/settings.json

# Create initial README content
cat << EOF > README.md
# Launch

Launch is a project designed to simplify the process of setting up and configuring a Linux system, specifically targeting new Linux users transitioning from other operating systems.

## Features

1. Guided, interactive setup process
2. Curated selection of essential free software
3. Automated system optimization
4. User-friendly interface for customization
5. Educational resources integrated into the setup process

## Getting Started

(Instructions on how to use Launch will be added here)

## Contributing

(Information for contributors will be added here)

## License

(License information will be added here)
EOF

# Create initial launch script
cat << EOF > bin/launch
#!/bin/bash

echo "Welcome to Launch!"
echo "This script will guide you through setting up your Linux system."
# Add more functionality here
EOF

# Make launch script executable
chmod +x bin/launch

# Create initial ASCII art file
cat << EOF > lib/ascii.sh
#!/bin/bash

display_ascii_art() {
    echo "
    _                           _     
   | |                         | |    
   | |     __ _ _   _ _ __   ___| |__  
   | |    / _\` | | | | '_ \\ / __| '_ \\ 
   | |___| (_| | |_| | | | | (__| | | |
   |______\\__,_|\\__,_|_| |_|\\___|_| |_|
                                       
    "
}

display_ascii_art
EOF

# Create initial main playbook
cat << EOF > playbooks/main.yml
---
- name: Main Launch playbook
  hosts: localhost
  connection: local
  become: yes

  roles:
    # Add roles here
EOF

# Create initial user guide
cat << EOF > docs/user_guide.md
# Launch User Guide

Welcome to Launch! This guide will help you get started with using Launch to set up your Linux system.

## Table of Contents

1. Introduction
2. Getting Started
3. Features
4. Troubleshooting
5. FAQ

(More content will be added here)
EOF

# Create VS Code settings
cat << EOF > .vscode/settings.json
{
  "files.associations": {
    "*.yml": "ansible",
    "*.yaml": "ansible"
  },
  "editor.insertSpaces": true,
  "editor.tabSize": 2,
  "editor.rulers": [80, 120],
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true
}
EOF

# Create .gitignore
cat << EOF > .gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/

# VS Code
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
EOF

echo "Repository structure created successfully!"
