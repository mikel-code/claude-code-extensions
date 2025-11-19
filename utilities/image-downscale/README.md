# Obsidian Image Downscaler - Claude Code Skill

A Claude Code skill for interactively downscaling large images in Obsidian vaults while preserving text readability.

## Features

- 🔍 **Smart filtering** - Only processes images above size/dimension thresholds
- 💬 **Interactive mode** - Review each image before processing
- 💾 **Safe backups** - Automatically backs up originals before replacing
- 📝 **Text preservation** - Uses hybrid method optimized for screenshots and documents
- 📊 **Progress tracking** - Shows space saved for each image and total
- ⚡ **Lightweight** - No AI dependencies, just Pillow + NumPy

## Quick Start

### 1. Install

```bash
cd image-downscale-skill
bash setup.sh
```

### 2. Use

```bash
cd /path/to/your/obsidian/vault
uv run python /path/to/image-downscale-skill/scripts/obsidian_processor.py
```

See [SKILL.md](SKILL.md) for complete documentation.

## Usage with Claude Code

When using this as a Claude Code skill, place it in your skills directory:

```bash
# Option 1: Clone/copy to skills directory
cp -r image-downscale-skill ~/.claude/skills/

# Option 2: Symlink to keep it version controlled elsewhere
ln -s /path/to/image-downscale-skill ~/.claude/skills/image-downscale-skill
```

Then in Claude Code, you can say:
- "Downscale images in my Obsidian vault"
- "Reduce image sizes in my vault"
- "Process large images in my vault"

## Configuration

Default settings:
- **Max width**: 1200px
- **File size threshold**: > 500 KB
- **Dimension threshold**: > 1200px (width or height)
- **Method**: Hybrid (pre-sharpening + Lanczos + post-sharpening)
- **Quality**: 95% (high quality JPEG)

Customize by editing the constants in `scripts/obsidian_processor.py`.

## Files

```
image-downscale-skill/
├── SKILL.md                    # Main skill documentation
├── README.md                   # This file
├── pyproject.toml              # Python dependencies
├── setup.sh                    # Setup script
├── scripts/
│   ├── downscale_core.py      # Core downscaling logic
│   └── obsidian_processor.py  # Main vault processor
└── references/
    └── usage-guide.md         # Detailed usage guide
```

## Requirements

- Python 3.9+
- uv package manager (installed by setup.sh if needed)
- Dependencies: Pillow, NumPy

## How It Works

1. Scans vault recursively for image files (png, jpg, jpeg, webp, etc.)
2. Filters to only images exceeding size or dimension thresholds
3. For each large image:
   - Shows current and projected size
   - Asks whether to process
   - Backs up original to `.image-backups/YYYY-MM-DD/`
   - Downscales using hybrid method
   - Replaces original file
4. Reports total space saved

## Safety

- **Backups first**: Always creates backups before modifying files
- **Atomic operations**: Uses temp files and rename (prevents corruption)
- **Error recovery**: Restores from backup if processing fails
- **Dry-run mode**: Preview what would happen without making changes
- **Interactive by default**: You approve each image

## 👩‍💻 Development

### Requirements

- Python 3.9+ (Python 3.12 recommended)
- uv package manager

### Setup Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd image-downscale-skill

# Install all dependencies including dev tools
uv sync --all-groups

# This installs:
# - Core: Pillow, NumPy
# - Dev tools: Ruff, Mypy, pytest
```

### Code Quality Tools

**Ruff** - Lightning-fast linter and formatter
```bash
# Check code for issues
uv run ruff check .

# Auto-fix issues
uv run ruff check . --fix

# Format code
uv run ruff format .
```

**Mypy** - Static type checker
```bash
# Type check the scripts
uv run mypy scripts/
```

### Development Workflow

1. **Make changes** to the code
2. **Format** with `uv run ruff format .`
3. **Lint** with `uv run ruff check . --fix`
4. **Type check** with `uv run mypy scripts/`
5. **Test** manually or add automated tests
6. **Commit** with clear messages

### Code Style

- Line length: 100 characters
- Use modern Python idioms (Python 3.9+)
- Type hints are encouraged
- Follow PEP 8 with Ruff's defaults

## License

Open source - use freely for personal or commercial projects.

## Credits

Downscaling method adapted from the [image-downscale](https://github.com/yourusername/image-downscale) project.
