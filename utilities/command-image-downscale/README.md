# Image Downscaler - Claude Code Command

A Claude Code command for downscaling large images while preserving text readability. Perfect for optimizing screenshots, diagrams, and high-resolution images in your notes and documents.

## Features

- 🎯 **Context-aware** - Works on specific images you're editing
- 💾 **Safe backups** - Automatically backs up originals before replacing
- 📝 **Text preservation** - Uses hybrid method optimized for screenshots and documents
- ⚡ **Lightweight** - Only processes what you specify
- 🔧 **Flexible** - Use as Claude Code command, standalone script, or batch utility

## Use Cases

### As Claude Code Command
- **Context-aware**: Optimize 1-3 specific images you're actively working with
- After pasting screenshots into Obsidian notes
- Optimizing images referenced in a document
- Part of your writing workflow

### As Standalone Script
- **Direct conversion**: Process individual images programmatically
- Integration into your own scripts or workflows
- One-off image optimization tasks
- Command-line batch processing with custom logic

## Quick Start

### Option 1: Claude Code Command

1. **Install dependencies:**
   ```bash
   cd command-image-downscale
   bash setup.sh
   ```

2. **Symlink the command directory:**

   **Global installation** (available in all projects):
   ```bash
   ln -s $(pwd) ~/.claude/commands/image-downscale
   ```

   **Project-specific installation**:
   ```bash
   mkdir -p .claude/commands
   ln -s $(pwd) .claude/commands/image-downscale
   ```

   This symlinks the entire directory with:
   - `image-downscale.md` (command definition)
   - `scripts/` (Python utilities)
   - All necessary dependencies

3. **Use in Claude Code:**
   ```
   /image-downscale path/to/image.png
   "Optimize the screenshot I just pasted"
   "Downscale images in this note"
   ```

### Option 2: Standalone Script

1. **Install dependencies** (same as above)

2. **Process a single image:**
   ```bash
   cd command-image-downscale
   uv run python scripts/downscale_core.py input.png output.png
   ```

3. **Use in your own scripts:**
   ```bash
   #!/bin/bash
   # Process images with custom logic
   for img in screenshots/*.png; do
     uv run python /path/to/scripts/downscale_core.py "$img" "$img"
   done
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

## Configuration

**Default settings:**
- **Max width**: 1200 px (maintains aspect ratio)
- **Quality**: 95% JPEG quality
- **Method**: Hybrid (pre-sharpen + Lanczos + post-sharpen)

**Command thresholds:**
- **File size**: > 500 KB
- **Dimensions**: > 1200 px (width or height)

For standalone script usage, specify max width as CLI argument:
```bash
uv run python scripts/downscale_core.py input.png output.png
# Uses default 1200px width

# Custom max width would require modifying the script or using batch_processor.py
```

## Advanced: Batch Processing Utility

For bulk vault maintenance or directory-wide processing, use the `batch_processor.py` utility:

**Features:**
- Interactive prompts for each image
- Directory scanning with threshold filtering
- Automatic backup creation
- Dry-run mode and auto-process option

**Usage:**
```bash
# Process entire directory (interactive prompts)
cd ~/your-vault
uv run python /path/to/scripts/batch_processor.py

# Process specific directory
uv run python scripts/batch_processor.py /path/to/images

# Dry run to preview changes
uv run python scripts/batch_processor.py --dry-run

# Auto-process all without prompts
uv run python scripts/batch_processor.py --yes

# Custom max width
uv run python scripts/batch_processor.py --max-width 1600
```

**Configuration:**
Edit constants in `scripts/batch_processor.py`:
```python
SIZE_THRESHOLD_KB = 500
DIMENSION_THRESHOLD_PX = 1200
DEFAULT_MAX_WIDTH = 1200
```

**Use cases:**
- Initial vault optimization
- Periodic cleanup (cron job)
- Processing hundreds of images at once
- Scheduled maintenance scripts

## Files

```
command-image-downscale/
├── image-downscale.md        # Command definition for Claude Code
├── README.md                  # This file (complete documentation)
├── pyproject.toml             # Python dependencies
├── setup.sh                   # Setup script
└── scripts/
    ├── downscale_core.py     # Core downscaling logic (used by command)
    └── batch_processor.py    # Batch utility for directory processing
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

### Standalone Script Example
```bash
$ uv run python scripts/downscale_core.py screenshot.png screenshot.png
Downscaling: screenshot.png
Original: 3840x2160 (2.4 MB)
Output: 1200x675 (410.0 KB)
Saved: 2.0 MB
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
