# Image Downscaler - Usage Guide

## Quick Start

### 1. First-Time Setup

```bash
cd /path/to/skill-image-downscale
bash setup.sh
```

This only needs to be done once. It will:
- Install `uv` if not present
- Create a virtual environment (`.venv/`)
- Install Pillow and NumPy

### 2. Process Your Images

```bash
cd /path/to/your/image/directory
uv run python /path/to/skill-image-downscale/scripts/image_processor.py
```

Or from anywhere:
```bash
uv run python /path/to/skill-image-downscale/scripts/image_processor.py /path/to/directory
```

**Use Cases:**
- Obsidian vault: `/path/to/my-vault`
- Presentation slides: `/path/to/presentation-exports`
- Web assets: `/path/to/website/images`
- Documentation: `/path/to/docs/screenshots`

## Common Usage Patterns

### Preview Mode (Dry Run)

See what would be processed without making any changes:

```bash
uv run python scripts/image_processor.py --dry-run
```

### Auto-Process All

Skip interactive prompts and process all large images:

```bash
uv run python scripts/image_processor.py --yes
```

**Warning**: This will process ALL images over the threshold. Use `--dry-run` first to preview!

### Custom Max Width

Change the target width for downscaling:

```bash
# For smaller images (800px wide - good for web/mobile)
uv run python scripts/image_processor.py --max-width 800

# For larger images (1600px wide - good for presentations/high-DPI)
uv run python scripts/image_processor.py --max-width 1600
```

### Combining Options

```bash
# Dry run with custom width
uv run python scripts/image_processor.py --dry-run --max-width 1000

# Auto-process with custom width
uv run python scripts/image_processor.py --yes --max-width 1400
```

## Configuration

### Per-Directory Configuration (Recommended)

Create a `.image-downscale.json` file in your target directory for custom settings:

```json
{
  "scan_paths": ["07/Organized/Images", "Attachments"],
  "max_width": 1200,
  "size_threshold_kb": 500,
  "dimension_threshold_px": 1200
}
```

**Key Features:**
- **scan_paths**: Only scan specific subdirectories (leave empty to scan all)
- **Automatic loading**: No CLI flags needed, just `cd` to the directory
- **Optional**: All fields optional, use only what you need
- **CLI override**: Command-line arguments always take precedence

**Quick Setup:**
```bash
cd ~/second-brain
cp ~/.claude/skills/skill-image-downscale/.image-downscale.json.example .image-downscale.json
# Edit with your preferred settings
```

### Understanding Thresholds

Images are only processed if they exceed ANY of these (configurable via `.image-downscale.json`):

- **File Size**: > 500 KB (default)
- **Width**: > 1200 px (default)
- **Height**: > 1200 px (default)

### Global Defaults (Alternative)

To change defaults for all directories, edit `scripts/image_processor.py`:

```python
SIZE_THRESHOLD_KB = 500        # Change file size threshold
DIMENSION_THRESHOLD_PX = 1200  # Change dimension threshold
DEFAULT_MAX_WIDTH = 1200       # Change default max width
```

## Interactive Mode Details

When processing interactively, for each image you'll see:

```
Image 1/12: attachments/screenshot.png
  Current: 3840x2160 (2.4 MB)
  Would downscale to: 1200x675 (~410.0 KB)
  Estimated savings: 2.0 MB

  Process this image? [y/n/skip-all/quit]:
```

Your options:
- `y` or `yes` - Process this image
- `n` or `no` - Skip this image
- `skip-all` or `s` - Skip this and all remaining images
- `quit` or `q` - Stop processing immediately

## Backup System

Every processed image is backed up before being replaced:

```
my-images/
├── .image-backups/
│   └── 2024-01-19/           # Date of processing
│       └── subfolder/
│           └── screenshot.png # Original image
└── subfolder/
    └── screenshot.png         # Downscaled image
```

### Restoring Backups

Restore a single image:
```bash
cp .image-backups/2024-01-19/attachments/image.png attachments/image.png
```

Restore all images from a session:
```bash
cp -r .image-backups/2024-01-19/* .
```

View all backup dates:
```bash
ls .image-backups/
```

Delete old backups after confirming everything is OK:
```bash
rm -rf .image-backups/2024-01-19/
```

## Tips & Best Practices

### 1. Always Dry Run First

Before processing a directory for the first time:
```bash
uv run python scripts/image_processor.py --dry-run
```

Review the list of images that would be processed. If it looks good, run without `--dry-run`.

### 2. Process Regularly

Run this periodically as you add new images to your directories. Only new large images will be processed.

### 3. Check File References

After processing, file references will still work since we replace the files in-place. For Obsidian users with markdown links:

```bash
# Search for image links (in directory root)
grep -r "!\[\[.*\]\]" *.md
```

### 4. Adjust Max Width Based on Use Case

- **For web/mobile viewing**: 800-1000px
- **For desktop reading**: 1200-1400px (default)
- **For high-DPI displays**: 1600-2000px

### 5. Keep Backups for a Week

After processing, wait a week to make sure everything looks good in your vault, then delete the backup folder to reclaim space.

## Troubleshooting

### Images Look Blurry

Try increasing the max width:
```bash
uv run python scripts/image_processor.py --max-width 1600
```

Or restore from backups and try a different downscaling method (would require modifying the script).

### "No module named 'PIL'"

Dependencies not installed. Run:
```bash
cd /path/to/skill-image-downscale
uv sync
```

### Script is Slow

The hybrid method processes ~2-5 images per second. For directories with many images:

1. Use `--dry-run` first to count images
2. Consider processing in smaller batches
3. Use `--yes` to avoid waiting for prompts

### Need to Change Python Version

Edit `.python-version`:
```bash
echo "3.11" > .python-version
```

Then reinstall:
```bash
rm -rf .venv uv.lock
uv sync
```

## Advanced Usage

### Test on a Single Image

```bash
cd scripts
uv run python downscale_core.py /path/to/input.png /path/to/output.png
```

### Batch Process Multiple Directories

```bash
for dir in ~/Documents/*/; do
    echo "Processing: $dir"
    uv run python scripts/image_processor.py "$dir" --yes
done
```

### Create a Shell Alias

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias image-downscale='uv run python /path/to/skill-image-downscale/scripts/image_processor.py'
```

Then use:
```bash
cd /path/to/images
image-downscale --dry-run
```

## Performance

- **Processing speed**: ~0.1-0.5 seconds per image
- **Memory usage**: ~100-200 MB
- **Typical results**: 50-80% file size reduction for screenshots
- **Quality**: Text remains fully readable at target size

## Getting Help

View all options:
```bash
uv run python scripts/image_processor.py --help
```

Report issues or contribute at: [project repository]
