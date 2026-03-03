#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

BOOTSTRAP_ENV = "NANO_BANANA_BOOTSTRAPPED"
CACHE_ROOT = Path.home() / ".cache" / "nano-banana"
VENV_DIR = CACHE_ROOT / ".venv"
DEPS_STAMP = CACHE_ROOT / ".deps_installed"
SCRIPT_DIR = Path(__file__).parent

DEFAULT_MODEL = "gemini-3.1-flash-image-preview"
DEFAULT_RESOLUTION = "2K"
DEFAULT_ASPECT_RATIO = "16:9"
DEFAULT_OUTPUT_DIR = "assets/generated"

MIME_TO_EXT = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/webp": ".webp",
}


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate images with Google Gemini")
    parser.add_argument("prompt", nargs="?", type=str, help="Image generation prompt")
    parser.add_argument(
        "--model", type=str, default=DEFAULT_MODEL,
        help=f"Gemini model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--resolution", type=str, default=DEFAULT_RESOLUTION,
        choices=["1K", "2K", "4K"],
        help=f"Output resolution (default: {DEFAULT_RESOLUTION})",
    )
    parser.add_argument(
        "--aspect", type=str, default=DEFAULT_ASPECT_RATIO,
        help=f"Aspect ratio (default: {DEFAULT_ASPECT_RATIO})",
    )
    parser.add_argument(
        "--output", type=str, default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--reference", type=str, action="append", default=[],
        help="Reference image path (can specify multiple, up to 14)",
    )
    return parser.parse_args(args)


def in_bootstrap_venv() -> bool:
    executable = Path(sys.executable).resolve()
    venv_root = VENV_DIR.resolve()
    try:
        executable.relative_to(venv_root)
        return True
    except ValueError:
        return False


def ensure_bootstrap() -> None:
    if os.environ.get(BOOTSTRAP_ENV) == "1":
        return
    if in_bootstrap_venv():
        return

    python_path = VENV_DIR / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    needs_venv = not python_path.exists()
    needs_install = needs_venv or not DEPS_STAMP.exists()

    try:
        CACHE_ROOT.mkdir(parents=True, exist_ok=True)
        if needs_venv:
            print("[Info] Creating virtual environment...")
            subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])
        if needs_install:
            print("[Info] Installing dependencies...")
            subprocess.check_call([
                str(python_path), "-m", "pip", "install", "-q",
                "google-genai", "Pillow", "python-dotenv",
            ])
            DEPS_STAMP.write_text("google-genai,Pillow,python-dotenv\n", encoding="utf-8")
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"[Error] Failed to bootstrap dependencies: {exc}", file=sys.stderr)
        print("[Info] Ensure Python can create venvs and has internet access.", file=sys.stderr)
        raise SystemExit(1) from exc

    env = os.environ.copy()
    env[BOOTSTRAP_ENV] = "1"
    os.execve(
        str(python_path),
        [str(python_path), str(Path(__file__).resolve()), *sys.argv[1:]],
        env,
    )


def get_api_key() -> str:
    from dotenv import load_dotenv
    load_dotenv(SCRIPT_DIR / ".env")

    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        print("[Error] GEMINI_API_KEY not set.", file=sys.stderr)
        print("[Info] Set it in scripts/.env or as an environment variable.", file=sys.stderr)
        print("[Info] Get a key at: https://aistudio.google.com/apikey", file=sys.stderr)
        sys.exit(1)
    return key


def get_output_path(output_dir: str, mime_type: str = "image/png") -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = MIME_TO_EXT.get(mime_type, ".png")
    return output_path / f"{timestamp}{ext}"


def generate_image(
    prompt: str,
    model: str,
    resolution: str,
    aspect_ratio: str,
    output_dir: str,
    reference_images: list[str] | None = None,
) -> str | None:
    from google import genai
    from google.genai import types
    from PIL import Image

    if reference_images:
        for image_path in reference_images:
            if not Path(image_path).exists():
                print(f"[Error] Reference image not found: {image_path}")
                return None

    client = genai.Client()

    if reference_images:
        contents: list = []
        for image_path in reference_images:
            img = Image.open(image_path)
            contents.append(img)
        contents.append(prompt)
    else:
        contents = prompt

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=resolution,
            ),
        ),
    )

    for part in response.parts:
        if part.text is not None:
            print(f"[Info] {part.text}")
        elif part.inline_data is not None:
            mime_type = part.inline_data.mime_type or "image/png"
            image = part.as_image()
            output_path = get_output_path(output_dir, mime_type)
            image.save(str(output_path))
            print(f"[Success] Image saved: {output_path}")
            return str(output_path)

    print("[Warning] Response contained no image data")
    return None


def main() -> int:
    args = parse_args()

    if not args.prompt:
        parse_args(["--help"])
        return 1

    ensure_bootstrap()

    get_api_key()

    if args.reference and len(args.reference) > 14:
        print("[Error] Maximum 14 reference images allowed")
        return 1

    try:
        result = generate_image(
            prompt=args.prompt,
            model=args.model,
            resolution=args.resolution,
            aspect_ratio=args.aspect,
            output_dir=args.output,
            reference_images=args.reference if args.reference else None,
        )
        if result is None:
            return 1
    except Exception as e:
        print(f"[Error] Image generation failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
