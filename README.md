# Nano Banana

A Claude Code skill for generating images with Gemini 3.1 Flash Image.

Ask Claude to generate an image. It handles the prompt engineering, API call, and saves the result. Supports text-to-image, editing with reference images, character consistency across scenes, and model selection.

## Install

```bash
# Install for current project only
curl -sSL https://raw.githubusercontent.com/azamat1ch/nano-banana/main/install.sh | bash

# Install globally (available in all projects)
curl -sSL https://raw.githubusercontent.com/azamat1ch/nano-banana/main/install.sh | bash -s -- --global
```

Restart Claude Code after installing.

## Setup

You need a `GEMINI_API_KEY` from [aistudio.google.com/apikey](https://aistudio.google.com/apikey) (free).

On first run, if the key isn't set, Claude will tell you exactly what command to run to save it. You can also set it yourself:

```bash
export GEMINI_API_KEY=your-key-here
```

## How It Works

Type `/nano-banana` in Claude Code.

**First run:** Claude checks for your API key and walks you through setup if needed. Dependencies install automatically into `~/.cache/nano-banana/.venv`.

**Every run after:** Describe what you want, get an image. Claude reads the built-in prompting guide (text rendering, character consistency, layout control, storyboarding) so you get good results without writing elaborate prompts yourself.

```
/nano-banana a watercolor painting of a cat playing piano
/nano-banana change the background to sunset --reference ./photo.png
/nano-banana same character, different pose --reference ./face.png --reference ./pose.png
```

## What It Can Do

**Text-to-image.** Describe what you want in natural language. The prompting guide helps Claude craft detailed prompts from simple descriptions.

**Image editing.** Pass reference images to change backgrounds, transfer styles, or match poses. No manual masking needed.

**Character consistency.** Up to 14 reference images for identity locking. Same character across different scenes, angles, and expressions.

**Text rendering.** Headlines, infographics, diagrams with specified fonts and placement.

**Model selection.** Default is `gemini-3.1-flash-image-preview`. Switch with `--model` for any Gemini image model.

## Requirements

- Claude Code
- Python 3.10+
- `GEMINI_API_KEY` (free, see [Setup](#setup))
