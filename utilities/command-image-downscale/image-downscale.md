# Image Downscale Command

Downscale large images while preserving text readability using the hybrid method (pre-sharpening + Lanczos + post-sharpening). Perfect for optimizing screenshots, diagrams, and high-resolution images in your notes.

## Task

When the user asks to downscale, optimize, or reduce the size of image(s):

1. **Identify the target images** from the user's request:
   - Explicit paths: `/image-downscale path/to/image.png`
   - File references: "optimize screenshot.png"
   - Context clues: "the image I just pasted", "images in this note"

2. **For each image:**
   - Use Read tool to check if it exists
   - Get file size and dimensions using Python/PIL
   - If it exceeds thresholds (>500KB or >1200px), proceed to downscale
   - Otherwise, inform user it's already optimized

3. **Downscale using the Python utility:**
   ```bash
   cd <command-directory>
   uv run python scripts/downscale_core.py <input-path> <output-path>
   ```

   **⚠️ CRITICAL:** ALWAYS use `uv run python`, never plain `python`

4. **Create backup** before replacing:
   - Copy original to `.image-backups/<date>/`
   - Then replace original with downscaled version

5. **Report results:**
   - Show before/after dimensions and file sizes
   - Report space saved
   - Confirm backup location

## Thresholds

Only process images that exceed ANY of:
- File size > 500 KB
- Width > 1200 px
- Height > 1200 px

Target: Max width of 1200px (maintains aspect ratio)

## Safety

- **Always backup** original images first
- **Atomic operations**: Write to temp file, then rename
- **Error handling**: Restore from backup if processing fails

## Example Usage

```
User: /image-downscale attachments/screenshot-2024.png

You: I'll downscale that image for you.
[checks size: 3840x2160, 2.4 MB]
[creates backup]
[downscales to 1200x675]
[replaces original]

Result:
✓ Downscaled: 3840x2160 → 1200x675
✓ Size reduced: 2.4 MB → 410 KB
✓ Space saved: 2.0 MB
✓ Backup: .image-backups/2024-11-19/attachments/screenshot-2024.png
```

```
User: Optimize the images in this note

You: I'll check the images referenced in this note.
[scans note for image references]
[finds 3 images, 2 need optimization]
[processes each one]

Results:
✓ image1.png: 2.1 MB → 380 KB (saved 1.7 MB)
✓ image2.png: Already optimized (skipped)
✓ diagram.png: 1.8 MB → 420 KB (saved 1.4 MB)
Total space saved: 3.1 MB
```

## Notes

- This command works on individual images or small batches
- For bulk vault optimization, use the Python script directly
- The Python utility in `scripts/` can also be run standalone for maintenance
