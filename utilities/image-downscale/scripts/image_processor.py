#!/usr/bin/env python3
"""
Interactive image processor for batch downscaling.

Scans a directory recursively for large images and prompts for each one to downscale.
Perfect for Obsidian vaults, presentation slides, web assets, and documentation.
Backs up originals before replacing them.
"""

import shutil
import sys
from datetime import datetime
from pathlib import Path

from downscale_core import downscale_image_file, format_bytes

# Configuration
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}
DEFAULT_MAX_WIDTH = 1200
SIZE_THRESHOLD_KB = 500
DIMENSION_THRESHOLD_PX = 1200


class ImageCandidate:
    """Represents an image that might need downscaling."""

    def __init__(self, path: Path, root_dir: Path):
        self.path = path
        self.root_dir = root_dir
        self.relative_path = path.relative_to(root_dir)
        self.file_size = path.stat().st_size

        # Get dimensions
        from PIL import Image

        with Image.open(path) as img:
            self.width, self.height = img.size

    @property
    def size_kb(self) -> float:
        return self.file_size / 1024

    @property
    def size_mb(self) -> float:
        return self.file_size / (1024 * 1024)

    def exceeds_threshold(
        self, size_kb: int = SIZE_THRESHOLD_KB, dimension_px: int = DIMENSION_THRESHOLD_PX
    ) -> bool:
        """Check if image exceeds size or dimension thresholds."""
        return self.size_kb > size_kb or self.width > dimension_px or self.height > dimension_px

    def calculate_downscaled_size(self, max_width: int) -> tuple[int, int]:
        """Calculate what the downscaled dimensions would be."""
        if self.width <= max_width:
            return (self.width, self.height)

        scale_factor = max_width / self.width
        return (max_width, int(self.height * scale_factor))

    def __str__(self) -> str:
        return (
            f"{self.relative_path}\n"
            f"  Size: {format_bytes(self.file_size)}\n"
            f"  Dimensions: {self.width} x {self.height}"
        )


def find_images(directory_path: Path) -> list[ImageCandidate]:
    """Find all images in the directory recursively."""
    images = []

    for ext in IMAGE_EXTENSIONS:
        for img_path in directory_path.rglob(f"*{ext}"):
            # Skip hidden folders and backup folders
            if any(part.startswith(".") for part in img_path.parts):
                continue

            try:
                candidate = ImageCandidate(img_path, directory_path)
                images.append(candidate)
            except Exception as e:
                print(f"Warning: Could not process {img_path}: {e}")

    return images


def create_backup(image_path: Path, root_dir: Path, backup_date: str) -> Path:
    """
    Create a backup of the original image.

    Args:
        image_path: Path to the image
        root_dir: Root directory being processed
        backup_date: Date string for backup folder (YYYY-MM-DD)

    Returns:
        Path to the backup file
    """
    relative_path = image_path.relative_to(root_dir)
    backup_dir = root_dir / ".image-backups" / backup_date
    backup_path = backup_dir / relative_path

    # Create backup directory
    backup_path.parent.mkdir(parents=True, exist_ok=True)

    # Copy file
    shutil.copy2(image_path, backup_path)

    return backup_path


def process_directory(
    directory_path: Path,
    max_width: int = DEFAULT_MAX_WIDTH,
    dry_run: bool = False,
    auto_yes: bool = False,
) -> None:
    """
    Interactively process images in a directory.

    Args:
        directory_path: Path to the directory to process
        max_width: Maximum width for downscaled images
        dry_run: If True, don't actually modify files
        auto_yes: If True, process all without prompting
    """
    if not directory_path.exists():
        print(f"Error: Directory not found at {directory_path}")
        sys.exit(1)

    print(f"Scanning directory: {directory_path}")
    print("=" * 80)

    # Find all images
    all_images = find_images(directory_path)
    print(f"Found {len(all_images)} total images")

    # Filter to candidates that exceed thresholds
    candidates = [img for img in all_images if img.exceeds_threshold()]

    if not candidates:
        print("No images exceed the size or dimension thresholds.")
        print(f"Thresholds: >{SIZE_THRESHOLD_KB}KB or >{DIMENSION_THRESHOLD_PX}px")
        return

    print(f"Found {len(candidates)} images exceeding thresholds:\n")

    # Prepare backup date
    backup_date = datetime.now().strftime("%Y-%m-%d")

    # Statistics
    processed_count = 0
    skipped_count = 0
    total_saved = 0

    # Process each candidate
    for i, candidate in enumerate(candidates, 1):
        print(f"\nImage {i}/{len(candidates)}: {candidate.relative_path}")
        print(
            f"  Current: {candidate.width}x{candidate.height} ({format_bytes(candidate.file_size)})"
        )

        new_width, new_height = candidate.calculate_downscaled_size(max_width)
        estimated_size = (
            candidate.file_size * (new_width * new_height) / (candidate.width * candidate.height)
        )

        if new_width < candidate.width:
            print(
                f"  Would downscale to: {new_width}x{new_height} (~{format_bytes(int(estimated_size))})"
            )
            estimated_savings = candidate.file_size - estimated_size
            print(f"  Estimated savings: {format_bytes(int(estimated_savings))}")
        else:
            print("  Already within max width, would optimize only")

        # Prompt user
        if auto_yes:
            response = "y"
        elif dry_run:
            response = "skip"
        else:
            response = input("\n  Process this image? [y/n/skip-all/quit]: ").lower()

        if response == "quit" or response == "q":
            print("\nQuitting...")
            break
        elif response == "skip-all" or response == "s":
            print("\nSkipping remaining images...")
            break
        elif response != "y" and response != "yes":
            print("  Skipped")
            skipped_count += 1
            continue

        if dry_run:
            print("  [DRY RUN] Would process this image")
            continue

        # Process the image
        try:
            # Create backup
            backup_path = create_backup(candidate.path, directory_path, backup_date)
            print(f"  ✓ Backed up to {backup_path.relative_to(directory_path)}")

            # Downscale to temporary location
            temp_path = candidate.path.with_suffix(candidate.path.suffix + ".tmp")
            result = downscale_image_file(candidate.path, temp_path, max_width=max_width)

            # Replace original
            temp_path.replace(candidate.path)

            bytes_saved = result["bytes_saved"]
            total_saved += bytes_saved

            print(f"  ✓ Downscaled: {result['target_size'][0]}x{result['target_size'][1]}")
            print(f"  ✓ Saved: {format_bytes(bytes_saved)}")

            processed_count += 1

        except Exception as e:
            print(f"  ✗ Error processing image: {e}")
            # Restore from backup if it exists
            if backup_path.exists():
                shutil.copy2(backup_path, candidate.path)
                print("  ✓ Restored from backup")
            continue

    # Print summary
    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"Processed: {processed_count} images")
    print(f"Skipped: {skipped_count} images")

    if not dry_run:
        print(f"Total space saved: {format_bytes(total_saved)}")
        if processed_count > 0:
            print(f"\nBackups stored in: {directory_path}/.image-backups/{backup_date}/")
            print("To restore an image:")
            print(f"  cp .image-backups/{backup_date}/path/to/image.png path/to/image.png")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Interactively downscale large images in a directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process current directory
  uv run python image_processor.py

  # Process specific directory
  uv run python image_processor.py /path/to/images

  # Use custom max width
  uv run python image_processor.py --max-width 1600

  # Dry run to see what would be processed
  uv run python image_processor.py --dry-run

  # Auto-process all without prompts
  uv run python image_processor.py --yes

Use Cases:
  - Obsidian vaults: Reduce storage while keeping notes readable
  - Presentations: Optimize exported slide images
  - Web assets: Compress images for faster loading
  - Documentation: Shrink screenshot-heavy docs

Thresholds (configurable in script):
  - File size: >{SIZE_THRESHOLD_KB}KB
  - Dimensions: >{DIMENSION_THRESHOLD_PX}px (width or height)
        """,
    )

    parser.add_argument(
        "directory_path",
        nargs="?",
        type=Path,
        default=Path.cwd(),
        help="Path to directory to process (default: current directory)",
    )

    parser.add_argument(
        "--max-width",
        type=int,
        default=DEFAULT_MAX_WIDTH,
        help=f"Maximum width in pixels (default: {DEFAULT_MAX_WIDTH})",
    )

    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be done without making changes"
    )

    parser.add_argument(
        "--yes", "-y", action="store_true", help="Auto-process all images without prompting"
    )

    args = parser.parse_args()

    print("Image Downscaler")
    print("=" * 80)
    print(f"Max width: {args.max_width}px")
    print("Method: Hybrid (pre+post sharpening)")
    print(
        f"Mode: {'DRY RUN' if args.dry_run else 'Interactive' if not args.yes else 'Auto-process'}"
    )
    print("")

    process_directory(
        args.directory_path, max_width=args.max_width, dry_run=args.dry_run, auto_yes=args.yes
    )


if __name__ == "__main__":
    main()
