---
name: image-downscale
description: Interactively downscale large images in any directory using the hybrid method for text preservation. Perfect for Obsidian vaults, presentations, web assets, and documentation. Backs up originals before replacing.
allowed-tools: Read, Write, Bash, Glob, AskUserQuestion
---

# Image Downscaler

**⚠️ CRITICAL: ALL Python commands MUST use `uv run` prefix**

This skill helps reduce the size of large images in any directory while preserving text readability using the hybrid downscaling method (pre-sharpening + Lanczos + post-sharpening). Perfect for optimizing images in Obsidian vaults, presentation slides, web assets, or any folder containing screenshots and documents.

## Features

- **Interactive mode**: Review each large image before processing
- **Safe backups**: Original images backed up to `.image-backups/` before replacing
- **Smart filtering**: Only prompts for images above size/dimension thresholds
- **Text preservation**: Uses hybrid method optimized for screenshots and documents
- **Space savings tracking**: Shows space saved for each image and total

## Prerequisites

First-time setup (only needs to be done once):

```bash
cd {baseDir}
bash setup.sh
```

This will:
1. Check if `uv` is installed (installs if needed)
2. Run `uv sync` to create virtual environment and install dependencies
3. Verify the installation

## Usage

### Basic Usage

To process images in a directory:

```bash
cd /path/to/image/directory
uv run python {baseDir}/scripts/image_processor.py
```

**IMPORTANT**: Always use `uv run python` - never use `python` directly!

### Options

```bash
# Process a specific directory
uv run python {baseDir}/scripts/image_processor.py /path/to/directory

# Use custom max width (default: 1200px)
uv run python {baseDir}/scripts/image_processor.py --max-width 1600

# Dry run to see what would be processed (safe preview)
uv run python {baseDir}/scripts/image_processor.py --dry-run

# Auto-process all without prompting
uv run python {baseDir}/scripts/image_processor.py --yes

# Get help
uv run python {baseDir}/scripts/image_processor.py --help
```

### Thresholds

Images are considered "large" if they exceed ANY of these thresholds:
- **File size**: > 500 KB
- **Width**: > 1200 px
- **Height**: > 1200 px

These can be customized by editing the constants at the top of `scripts/image_processor.py`.

## Workflow

1. **Scan**: Script scans the directory recursively for all images
2. **Filter**: Identifies images exceeding thresholds
3. **Interactive**: For each large image:
   - Shows current size and dimensions
   - Shows estimated output size and space savings
   - Prompts: `Process this image? [y/n/skip-all/quit]`
4. **Backup**: If you say yes, creates backup in `.image-backups/YYYY-MM-DD/`
5. **Process**: Downscales using hybrid method (preserves text)
6. **Replace**: Replaces original with downscaled version
7. **Summary**: Shows total images processed and space saved

## Example Session

```bash
$ cd ~/Documents/MyImages
$ uv run python ~/image-downscale/scripts/image_processor.py

Image Downscaler
================================================================================
Max width: 1200px
Method: Hybrid (pre+post sharpening)
Mode: Interactive

Scanning directory: /Users/mikel/Documents/MyImages
================================================================================
Found 45 total images
Found 12 images exceeding thresholds:

Image 1/12: attachments/screenshot-2024.png
  Current: 3840x2160 (2.4 MB)
  Would downscale to: 1200x675 (~410.0 KB)
  Estimated savings: 2.0 MB

  Process this image? [y/n/skip-all/quit]: y
  ✓ Backed up to .image-backups/2024-01-19/attachments/screenshot-2024.png
  ✓ Downscaled: 1200x675
  ✓ Saved: 2.0 MB

[... continues for each image ...]

================================================================================
Summary
================================================================================
Processed: 8 images
Skipped: 4 images
Total space saved: 12.3 MB

Backups stored in: /Users/mikel/Documents/MyImages/.image-backups/2024-01-19/
To restore an image:
  cp .image-backups/2024-01-19/path/to/image.png path/to/image.png
```

## Restoring Backups

If you need to restore an original image:

```bash
# Restore a specific image
cp .image-backups/2024-01-19/attachments/image.png attachments/image.png

# Restore all images from a date
cp -r .image-backups/2024-01-19/* .

# Delete backups after confirming everything looks good
rm -rf .image-backups/2024-01-19/
```

## Safety Features

- **Always backs up** originals before modifying
- **Atomic operations**: Writes to temp file, then renames (prevents corruption)
- **Error handling**: Restores from backup if processing fails
- **Dry-run mode**: Preview what would happen without making changes
- **Interactive by default**: You approve each image

## Configuration

### Option 1: Configuration File (Recommended)

Create a `.image-downscale.json` file in your target directory to customize behavior:

```json
{
  "scan_paths": ["07/Organized/Images", "Attachments"],
  "max_width": 1200,
  "size_threshold_kb": 500,
  "dimension_threshold_px": 1200
}
```

**Configuration Options:**
- `scan_paths`: Array of subdirectories to scan (relative to root). If empty/missing, scans entire directory
- `max_width`: Maximum width in pixels (CLI `--max-width` overrides this)
- `size_threshold_kb`: Only process images larger than this
- `dimension_threshold_px`: Only process images wider or taller than this

**Example:** For an Obsidian vault at `~/second-brain`, create `~/second-brain/.image-downscale.json`:
```json
{
  "scan_paths": ["07/Organized/Images"]
}
```

Then run from vault root:
```bash
cd ~/second-brain
uv run python {baseDir}/scripts/image_processor.py
```

**Behavior:**
- ✓ **With config & scan_paths**: Scans only specified subdirectories
- ✓ **With config but no scan_paths**: Scans entire directory
- ✓ **Without config**: Scans entire directory (backward compatible)
- ✓ **CLI path argument**: Always overrides config scan_paths

See `.image-downscale.json.example` in the skill directory for a complete example.

### Option 2: Edit Script Defaults

To change global defaults, edit `scripts/image_processor.py`:

```python
# Near the top of the file
SIZE_THRESHOLD_KB = 500        # File size threshold in KB
DIMENSION_THRESHOLD_PX = 1200  # Width/height threshold in pixels
DEFAULT_MAX_WIDTH = 1200       # Default max width for downscaling
```

## Command Reference

**❌ NEVER use these commands:**
- `python script.py` (will use wrong Python/environment)
- `pip install` (breaks uv environment)
- Direct execution without `uv run`

**✅ ALWAYS use these commands:**
- `uv run python scripts/image_processor.py`
- `uv add package-name` (to add dependencies)
- `uv sync` (to install/update dependencies)

## Troubleshooting

### "ModuleNotFoundError: No module named 'PIL'"

Dependencies not installed. Run:
```bash
cd {baseDir}
uv sync
```

### "No images exceed the size or dimension thresholds"

Your images are already small! You can:
- Lower the thresholds in `scripts/obsidian_processor.py`
- Or specify smaller max-width: `--max-width 800`

### "Error: uv is not installed"

Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then run `bash setup.sh` again.

### Restore all backups

If something went wrong and you want to restore everything:
```bash
# Go to vault
cd /path/to/vault

# Find the backup date
ls .image-backups/

# Restore all from that date
cp -r .image-backups/2024-01-19/* .
```

## For Claude Code

When the user asks to "downscale images" or "optimize images" or "reduce image sizes":

1. Ask where their image directory is located (could be Obsidian vault, presentation folder, web assets, etc.)
2. Offer to run in dry-run mode first to preview
3. Run: `uv run python {baseDir}/scripts/image_processor.py /path/to/directory --dry-run`
4. Show the results
5. If user approves, run without `--dry-run`
6. **CRITICAL**: Always use `uv run python`, never plain `python`

**Common use cases to recognize:**
- "Downscale images in my Obsidian vault" → Obsidian vault optimization
- "Optimize images in my presentation folder" → Presentation slide optimization
- "Reduce image sizes for web" → Web asset optimization
- "Process screenshots in this directory" → Documentation/screenshot optimization

## Technical Details

**Method**: Hybrid downscaling
- Light pre-sharpening (1.2x) to compensate for interpolation softening
- Lanczos-3 resampling for high-quality downscaling
- Light post-sharpening (0.8px radius, 120% strength) to enhance edges

**Dependencies**: Only Pillow and NumPy (lightweight, no AI/GPU required)

**Performance**: ~0.1-0.5 seconds per image on modern hardware

**Quality**: Optimized for text preservation - screenshots and documents remain readable after downscaling
