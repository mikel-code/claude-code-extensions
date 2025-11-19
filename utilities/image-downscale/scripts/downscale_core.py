#!/usr/bin/env python3
"""
Core image downscaling functionality using the hybrid method.

This module provides text-preserving downscaling optimized for screenshots
and documents commonly found in Obsidian vaults.
"""

from pathlib import Path
from typing import Optional

from PIL import Image, ImageEnhance, ImageFilter


def downscale_hybrid(
    image: Image.Image,
    target_size: tuple[int, int],
    pre_sharpen: float = 1.2,
    post_sharpen_radius: float = 0.8,
    post_sharpen_percent: int = 120,
) -> Image.Image:
    """
    Hybrid downscaling approach: light pre-sharpening + Lanczos + light post-sharpening.

    This method provides the best balance for text preservation:
    - Pre-sharpening compensates for interpolation softening
    - Lanczos resampling preserves high-frequency details
    - Post-sharpening enhances edge clarity

    Args:
        image: Input PIL Image
        target_size: (width, height) tuple for output
        pre_sharpen: Pre-sharpening intensity (1.0-1.5 recommended)
        post_sharpen_radius: Unsharp mask radius (0.5-1.0 recommended)
        post_sharpen_percent: Unsharp mask strength (100-150 recommended)

    Returns:
        Downscaled and sharpened image
    """
    # Light pre-sharpening
    enhancer = ImageEnhance.Sharpness(image)
    sharpened = enhancer.enhance(pre_sharpen)

    # Lanczos downscaling
    downscaled = sharpened.resize(target_size, Image.LANCZOS)

    # Light post-sharpening with unsharp mask
    final = downscaled.filter(
        ImageFilter.UnsharpMask(
            radius=post_sharpen_radius, percent=post_sharpen_percent, threshold=2
        )
    )

    return final


def calculate_target_size(
    current_size: tuple[int, int],
    max_width: Optional[int] = None,
    max_height: Optional[int] = None,
    scale: Optional[float] = None,
) -> tuple[int, int]:
    """
    Calculate target dimensions based on constraints.

    Args:
        current_size: Current (width, height)
        max_width: Maximum width (maintains aspect ratio)
        max_height: Maximum height (maintains aspect ratio)
        scale: Scale factor (e.g., 0.5 for 50%)

    Returns:
        Target (width, height) tuple
    """
    current_width, current_height = current_size

    if scale:
        return (int(current_width * scale), int(current_height * scale))

    if max_width and current_width > max_width:
        scale_factor = max_width / current_width
        return (max_width, int(current_height * scale_factor))

    if max_height and current_height > max_height:
        scale_factor = max_height / current_height
        return (int(current_width * scale_factor), max_height)

    # No downscaling needed
    return current_size


def downscale_image_file(
    input_path: Path,
    output_path: Path,
    max_width: int = 1200,
    max_height: Optional[int] = None,
    quality: int = 95,
) -> dict:
    """
    Downscale an image file using the hybrid method.

    Args:
        input_path: Path to input image
        output_path: Path to save output image
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels (optional)
        quality: JPEG quality (1-100)

    Returns:
        Dictionary with processing info:
        {
            'original_size': (width, height),
            'target_size': (width, height),
            'original_file_size': bytes,
            'output_file_size': bytes,
            'bytes_saved': bytes
        }
    """
    # Load image
    image = Image.open(input_path).convert("RGB")
    original_size = image.size
    original_file_size = input_path.stat().st_size

    # Calculate target size
    target_size = calculate_target_size(original_size, max_width=max_width, max_height=max_height)

    # Check if downscaling is needed
    if target_size == original_size:
        # No downscaling needed, just copy
        image.save(output_path, quality=quality, optimize=True)
    else:
        # Downscale with hybrid method
        downscaled = downscale_hybrid(image, target_size)
        downscaled.save(output_path, quality=quality, optimize=True)

    image.close()

    # Get output file size
    output_file_size = output_path.stat().st_size

    return {
        "original_size": original_size,
        "target_size": target_size,
        "original_file_size": original_file_size,
        "output_file_size": output_file_size,
        "bytes_saved": original_file_size - output_file_size,
    }


def format_bytes(bytes_val: int) -> str:
    """Format bytes into human-readable string."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} TB"


if __name__ == "__main__":
    # Quick test
    import sys

    if len(sys.argv) < 3:
        print("Usage: uv run python downscale_core.py <input> <output>")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    if not input_file.exists():
        print(f"Error: {input_file} not found")
        sys.exit(1)

    print(f"Downscaling: {input_file}")
    result = downscale_image_file(input_file, output_file)

    print(
        f"Original: {result['original_size'][0]}x{result['original_size'][1]} ({format_bytes(result['original_file_size'])})"
    )
    print(
        f"Output: {result['target_size'][0]}x{result['target_size'][1]} ({format_bytes(result['output_file_size'])})"
    )
    print(f"Saved: {format_bytes(result['bytes_saved'])}")
