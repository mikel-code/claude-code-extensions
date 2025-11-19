#!/bin/bash
# Setup script for Image Downscaler skill
# This installs uv (if needed) and dependencies

set -e

echo "=========================================="
echo "Image Downscaler - Setup"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}uv is not installed. Installing...${NC}"
    echo ""

    # Detect OS and install
    if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Installing uv via official installer..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        echo ""
        echo -e "${GREEN}✓ uv installed${NC}"
        echo ""
        echo "Please restart your terminal or run:"
        echo "  source \$HOME/.cargo/env"
        echo ""
        echo "Then run this setup script again."
        exit 0
    else
        echo -e "${RED}Unsupported operating system: $OSTYPE${NC}"
        echo "Please install uv manually from: https://github.com/astral-sh/uv"
        exit 1
    fi
else
    echo -e "${GREEN}✓ uv is installed${NC}"
fi

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo ""
echo "Installing dependencies..."
uv sync

echo ""
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Test that imports work
echo ""
echo "Verifying installation..."
if uv run python -c "from PIL import Image; import numpy; print('Imports successful')" 2>/dev/null; then
    echo -e "${GREEN}✓ Installation verified${NC}"
else
    echo -e "${RED}✗ Installation verification failed${NC}"
    echo "Please check the error messages above."
    exit 1
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Usage:"
echo "  cd /path/to/image/directory"
echo "  uv run python $SCRIPT_DIR/scripts/image_processor.py"
echo ""
echo "For help:"
echo "  uv run python $SCRIPT_DIR/scripts/image_processor.py --help"
echo ""
echo "See SKILL.md for full documentation."
echo ""
