# Nano Banana

A Claude Code skill for generating images with Gemini 3.1 Flash Image.

## Install

```bash
# Install for current project only
curl -sSL https://raw.githubusercontent.com/azamat1ch/nano-banana/main/install.sh | bash

# Install globally (available in all projects)
curl -sSL https://raw.githubusercontent.com/azamat1ch/nano-banana/main/install.sh | bash -s -- --global
```

Restart Claude Code after installing.

## Setup

You need a `GEMINI_API_KEY`. Get one at [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

Set it either as an environment variable or in `scripts/.env`:

```bash
# Option 1: environment variable
export GEMINI_API_KEY=your-key-here

# Option 2: .env file (persistent)
echo "GEMINI_API_KEY=your-key-here" > scripts/.env
```

If the key isn't set, the script tells you exactly what to do.

## Usage

Type `/nano-banana` in Claude Code, or run directly:

```bash
# Generate an image
python3 scripts/generate.py "a cat playing piano in watercolor style"

# High-res with custom aspect ratio
python3 scripts/generate.py "neon city street" --resolution 4K --aspect 16:9

# Edit an existing image
python3 scripts/generate.py "change background to sunset" --reference ./photo.png

# Multiple references for style transfer or character consistency
python3 scripts/generate.py "same person, new pose" --reference ./face.png --reference ./pose.png

# Use a different model
python3 scripts/generate.py "sunset coastline" --model gemini-2.0-flash-exp
```

## How It Works

First run bootstraps a virtual environment at `~/.cache/nano-banana/.venv` and installs dependencies automatically. No manual setup needed beyond the API key.

The skill includes a full prompting guide (text rendering, character consistency, layout control, storyboarding) that Claude reads when generating images, so you get good results without prompt engineering.

## What It Can Do

- **Text-to-image.** Describe what you want in natural language.
- **Image editing.** Pass reference images to change backgrounds, transfer styles, match poses.
- **Character consistency.** Up to 14 reference images for identity locking across scenes.
- **Text rendering.** Headlines, infographics, diagrams with specified fonts and placement.
- **Model selection.** Default is Gemini 3.1 Flash Image, switch with `--model`.

## Requirements

- Python 3.10+
- `GEMINI_API_KEY` (see [Setup](#setup))
