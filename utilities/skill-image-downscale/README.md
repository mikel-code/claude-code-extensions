# Image Downscaler - Claude Code Skill

A Claude Code skill for interactively downscaling large images while preserving text readability. Perfect for optimizing images in Obsidian vaults, presentation slides, web assets, or any directory containing screenshots and documents.

## Features

- 🔍 **Smart filtering** - Only processes images above size/dimension thresholds
- 💬 **Interactive mode** - Review each image before processing
- 💾 **Safe backups** - Automatically backs up originals before replacing
- 📝 **Text preservation** - Uses hybrid method optimized for screenshots and documents
- 📊 **Progress tracking** - Shows space saved for each image and total
- ⚡ **Lightweight** - No AI dependencies, just Pillow + NumPy

## Use Cases

- **Obsidian vaults** - Reduce storage while keeping notes readable
- **Presentation slides** - Optimize exported images for sharing
- **Web assets** - Compress images for faster loading
- **Documentation** - Shrink screenshot-heavy docs
- **Photo archives** - Downscale high-res images for everyday viewing

## Quick Start

### 1. Install

```bash
cd skill-image-downscale
bash setup.sh
```

### 2. Use

```bash
cd /path/to/your/image/directory
uv run python /path/to/skill-image-downscale/scripts/image_processor.py
```

See [SKILL.md](SKILL.md) for complete documentation.

## Usage with Claude Code

When using this as a Claude Code skill, place it in your skills directory:

```bash
# Option 1: Clone/copy to skills directory
cp -r skill-image-downscale ~/.claude/skills/

# Option 2: Symlink to keep it version controlled elsewhere
ln -s /path/to/skill-image-downscale ~/.claude/skills/skill-image-downscale
```

Then in Claude Code, you can say:
- "Downscale images in my directory"
- "Reduce image sizes in my Obsidian vault"
- "Optimize images in my presentation folder"
- "Process large images in this directory"

## Configuration

### Per-Directory Configuration (Recommended)

Create a `.image-downscale.json` file in your target directory:

```json
{
  "scan_paths": ["07/Organized/Images", "Attachments"],
  "max_width": 1200,
  "size_threshold_kb": 500,
  "dimension_threshold_px": 1200
}
```

**Benefits:**
- Scan only specific subdirectories (perfect for Obsidian vaults)
- Different settings per project/directory
- No need to modify the skill itself
- All options are optional - use only what you need

**Example for Obsidian:**
```bash
# Create config in your vault
cd ~/second-brain
cat > .image-downscale.json << 'EOF'
{
  "scan_paths": ["07/Organized/Images"]
}
EOF

# Now the skill only scans that directory
uv run python ~/.claude/skills/skill-image-downscale/scripts/image_processor.py
```

See `.image-downscale.json.example` for all options.

### Default Settings

- **Max width**: 1200px
- **File size threshold**: > 500 KB
- **Dimension threshold**: > 1200px (width or height)
- **Method**: Hybrid (pre-sharpening + Lanczos + post-sharpening)
- **Quality**: 95% (high quality JPEG)

## Files

```
skill-image-downscale/
├── SKILL.md                  # Main skill documentation
├── README.md                 # This file
├── pyproject.toml            # Python dependencies
├── setup.sh                  # Setup script
├── scripts/
│   ├── downscale_core.py    # Core downscaling logic
│   └── image_processor.py   # Main image processor
└── references/
    └── usage-guide.md       # Detailed usage guide
```

## Requirements

- Python 3.9+
- uv package manager (installed by setup.sh if needed)
- Dependencies: Pillow, NumPy

## How It Works

1. Scans directory recursively for image files (png, jpg, jpeg, webp, etc.)
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
cd skill-image-downscale

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
