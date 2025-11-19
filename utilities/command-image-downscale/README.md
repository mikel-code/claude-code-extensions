# Image Downscaler - Claude Code Command

A Claude Code command for downscaling large images while preserving text readability. Perfect for optimizing screenshots, diagrams, and high-resolution images in your notes and documents.

## Features

- 🎯 **Context-aware** - Works on specific images you're editing
- 💾 **Safe backups** - Automatically backs up originals before replacing
- 📝 **Text preservation** - Uses hybrid method optimized for screenshots and documents
- ⚡ **Lightweight** - Only processes what you specify
- 🔧 **Dual-purpose** - Use as command OR standalone Python utility

## Use Cases

### As Claude Code Command
- After pasting screenshots into Obsidian notes
- Optimizing images in a specific document
- Quick optimization of 1-3 images you're working with
- Part of your writing workflow

### As Standalone Utility
- Bulk vault maintenance (run script directly)
- Scheduled optimization (cron job)
- Processing entire directories
- Initial vault setup

## Quick Start

### Option 1: Claude Code Command

1. **Install dependencies:**
   ```bash
   cd command-image-downscale
   bash setup.sh
   ```

2. **Symlink the command:**
   ```bash
   ln -s $(pwd)/image-downscale.md ~/.claude/commands/image-downscale.md
   ```

3. **Use in Claude Code:**
   ```
   /image-downscale path/to/image.png
   "Optimize the screenshot I just pasted"
   "Downscale images in this note"
   ```

### Option 2: Standalone Python Utility

1. **Install dependencies** (same as above)

2. **Run directly:**
   ```bash
   cd /path/to/your/images
   uv run python /path/to/command-image-downscale/scripts/image_processor.py
   ```

3. **Or create a maintenance script:**
   ```bash
   #!/bin/bash
   # ~/second-brain/optimize-images.sh
   cd ~/second-brain
   uv run python ~/command-image-downscale/scripts/image_processor.py
   ```

## Command Usage

The `/image-downscale` command supports:

**Explicit paths:**
```
/image-downscale attachments/screenshot.png
/image-downscale img1.png img2.png img3.png
```

**Natural language:**
```
"Optimize the image I just pasted"
"Reduce the size of diagram.png"
"Downscale the images in this note"
```

**Behavior:**
- Checks if image exceeds thresholds (>500KB or >1200px)
- Creates backup before modifying
- Downscales using hybrid method
- Reports before/after stats

## Python Utility Usage

For bulk processing or maintenance:

```bash
# Process entire directory
uv run python scripts/image_processor.py

# Process specific directory
uv run python scripts/image_processor.py /path/to/images

# With custom settings
uv run python scripts/image_processor.py --max-width 1600 --dry-run

# Auto-process without prompts
uv run python scripts/image_processor.py --yes
```

## Configuration

**Default thresholds:**
- **File size**: > 500 KB
- **Dimensions**: > 1200 px (width or height)
- **Max width**: 1200 px (maintains aspect ratio)

To customize, edit constants in `scripts/image_processor.py`:
```python
SIZE_THRESHOLD_KB = 500
DIMENSION_THRESHOLD_PX = 1200
DEFAULT_MAX_WIDTH = 1200
```

Or use CLI arguments:
```bash
uv run python scripts/image_processor.py --max-width 1600
```

## Files

```
command-image-downscale/
├── image-downscale.md        # Command definition for Claude Code
├── README.md                  # This file (complete documentation)
├── pyproject.toml             # Python dependencies
├── setup.sh                   # Setup script
└── scripts/
    ├── downscale_core.py     # Core downscaling logic
    └── image_processor.py    # Utility for batch processing
```

## Requirements

- Python 3.9+
- uv package manager (installed by setup.sh if needed)
- Dependencies: Pillow, NumPy

## How It Works

### Hybrid Downscaling Method
1. **Pre-sharpening** (1.2x) - Compensates for interpolation softening
2. **Lanczos-3 resampling** - High-quality downscaling
3. **Post-sharpening** (UnsharpMask) - Enhances edge clarity

Result: Text and diagrams remain readable after downscaling

### Safety Features
- **Backups first**: Always creates backups before modifying
- **Atomic operations**: Uses temp files and rename (prevents corruption)
- **Error recovery**: Restores from backup if processing fails

## Examples

### Command Example
```
User: /image-downscale screenshot-2024.png

Claude: I'll downscale that image for you.
✓ Downscaled: 3840x2160 → 1200x675
✓ Size reduced: 2.4 MB → 410 KB
✓ Space saved: 2.0 MB
✓ Backup: .image-backups/2024-11-19/screenshot-2024.png
```

### Utility Example
```bash
$ cd ~/second-brain
$ uv run python ~/command-image-downscale/scripts/image_processor.py

Found 45 total images
Found 12 images exceeding thresholds

[Interactive processing...]

Processed: 8 images
Total space saved: 12.3 MB
```

## Development

### Setup Development Environment

```bash
cd command-image-downscale
uv sync --all-groups  # Installs dev tools: ruff, mypy, pytest
```

### Code Quality

```bash
# Lint and format
uv run ruff check . --fix
uv run ruff format .

# Type check
uv run mypy scripts/
```

## License

Open source - use freely for personal or commercial projects.
