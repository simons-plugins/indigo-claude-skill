#!/bin/bash

# Indigo Plugin Development Skill Installer
# This script helps you install the skill in your project

set -e

echo "============================================"
echo "Indigo Plugin Development Skill Installer"
echo "============================================"
echo

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}!${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if we're in a git repository
if git rev-parse --git-dir > /dev/null 2>&1; then
    PROJECT_ROOT=$(git rev-parse --show-toplevel)
    print_success "Found git repository at: $PROJECT_ROOT"
else
    PROJECT_ROOT=$(pwd)
    print_warning "Not in a git repository, using current directory: $PROJECT_ROOT"
fi

# Determine installation method
echo
echo "Choose installation method:"
echo "  1. Clone (copy skill into your project)"
echo "  2. Submodule (link skill as git submodule)"
echo "  3. Symlink (create symbolic link to skill)"
echo
read -p "Enter choice [1-3]: " choice

SKILL_DIR="$PROJECT_ROOT/.claude/skills/indigo"

case $choice in
    1)
        echo
        echo "Cloning skill repository..."
        mkdir -p "$PROJECT_ROOT/.claude/skills"

        if [ -d "$SKILL_DIR" ]; then
            print_warning "Skill directory already exists at: $SKILL_DIR"
            read -p "Remove and reinstall? [y/N]: " confirm
            if [[ $confirm == [yY] ]]; then
                rm -rf "$SKILL_DIR"
            else
                print_error "Installation cancelled"
                exit 1
            fi
        fi

        git clone https://github.com/indigo-community/indigo-skill.git "$SKILL_DIR"
        print_success "Skill cloned to: $SKILL_DIR"
        ;;

    2)
        echo
        echo "Adding skill as git submodule..."

        if [ ! -d "$PROJECT_ROOT/.git" ]; then
            print_error "Not in a git repository. Submodule installation requires git."
            exit 1
        fi

        mkdir -p "$PROJECT_ROOT/.claude/skills"

        if [ -d "$SKILL_DIR" ]; then
            print_warning "Skill directory already exists"
            exit 1
        fi

        git submodule add https://github.com/indigo-community/indigo-skill.git "$SKILL_DIR"
        git submodule update --init --recursive
        print_success "Skill added as submodule to: $SKILL_DIR"
        ;;

    3)
        echo
        echo "Creating symbolic link..."
        read -p "Enter path to cloned skill repository: " skill_source

        if [ ! -d "$skill_source" ]; then
            print_error "Directory not found: $skill_source"
            exit 1
        fi

        mkdir -p "$PROJECT_ROOT/.claude/skills"

        if [ -L "$SKILL_DIR" ] || [ -d "$SKILL_DIR" ]; then
            print_warning "Skill already exists at: $SKILL_DIR"
            read -p "Remove and reinstall? [y/N]: " confirm
            if [[ $confirm == [yY] ]]; then
                rm -rf "$SKILL_DIR"
            else
                print_error "Installation cancelled"
                exit 1
            fi
        fi

        ln -s "$skill_source" "$SKILL_DIR"
        print_success "Symlink created: $SKILL_DIR -> $skill_source"
        ;;

    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

# Verify installation
echo
echo "Verifying installation..."

if [ -f "$SKILL_DIR/skill.md" ]; then
    print_success "Skill file found"
else
    print_error "Skill file not found at: $SKILL_DIR/skill.md"
    exit 1
fi

if [ -d "$SKILL_DIR/docs" ]; then
    print_success "Documentation found"
else
    print_warning "Documentation directory not found"
fi

echo
echo "============================================"
print_success "Installation complete!"
echo "============================================"
echo
echo "Usage in Claude Code:"
echo "  /indigo \"How do I create a custom device?\""
echo "  /indigo \"Show me polling pattern examples\""
echo "  /indigo \"Debug this plugin lifecycle issue\""
echo
echo "Documentation available at:"
echo "  $SKILL_DIR/docs/"
echo
echo "For help:"
echo "  - Read the docs: $SKILL_DIR/docs/README.md"
echo "  - View examples: $SKILL_DIR/docs/examples/"
echo "  - Check README: $SKILL_DIR/README.md"
echo
