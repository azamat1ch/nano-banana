---
name: nano-banana
description: |
  Image generation using Gemini 3.1 Flash Image model.
  Use when the user needs to: (1) Generate images from text prompts, (2) Create visuals for LinkedIn posts, presentations, or content, (3) Generate logos, infographics, illustrations, or diagrams, (4) Edit existing images (background changes, style transfer, colorization), (5) Create consistent character/brand imagery across multiple images.
---

# Image Generation with Nano Banana

Generate images with Gemini 3.1 Flash Image. Text-to-image, editing with references, character consistency, and model selection.

## Command

```bash
python3 scripts/generate.py "prompt" [options]
```

**Options:**
| Flag | Values | Default |
|------|--------|---------|
| `--model` | any Gemini model string | gemini-3.1-flash-image-preview |
| `--resolution` | 1K, 2K, 4K | 2K |
| `--aspect` | 1:1, 16:9, 9:16, 4:3, etc. | 16:9 |
| `--output` | directory path | assets/generated |
| `--reference` | image path (up to 14) | - |

## Examples

```bash
# Basic generation
python3 scripts/generate.py "a cat playing piano in watercolor style"

# Specific model
python3 scripts/generate.py "sunset coastline" --model gemini-2.0-flash-exp

# High-res wide image
python3 scripts/generate.py "sunset coastline" --resolution 4K --aspect 16:9

# Custom output location
python3 scripts/generate.py "logo design" --output ./my-project/images

# Edit existing image
python3 scripts/generate.py "change background to sunset" --reference ./original.png

# Multiple references (style transfer, pose matching)
python3 scripts/generate.py "draw this person in this pose" --reference ./person.png --reference ./pose.png
```

## Prompting Guide

### Core Principles

**Use natural language, not tag soup.** Talk to it like briefing a human artist.

- Bad: `"Cool car, neon, city, night, 8k"`
- Good: `"A cinematic wide shot of a futuristic sports car speeding through a rainy Tokyo street at night. Neon signs reflect off wet pavement."`

**Include these elements:**
- **Subject**: Be specific ("a stoic robot barista with glowing blue eyes")
- **Composition**: How is it framed? (close-up, wide shot, low-angle, shallow depth of field)
- **Action**: What's happening?
- **Location**: Where? Be descriptive with atmosphere
- **Style**: Aesthetic (3D animation, film noir, watercolor, photorealistic, 1990s product photography)
- **Materiality**: Describe textures ("matte finish", "brushed steel", "soft velvet", "crumpled paper")

**Provide context (the "why")** - helps the model make logical artistic decisions:
- "Create an image of a sandwich for a high-end gourmet cookbook" → infers professional plating, shallow depth of field, perfect lighting

**Edit, don't re-roll** - if 80% correct, ask for specific changes rather than regenerating:
- "That's great, but change the lighting to sunset and make the text neon blue"

### Text & Infographics

The model has strong text rendering capabilities:
- Put exact text in quotes: `"place the headline 'URBAN EXPLORER' at the top"`
- Specify font style and placement: `"bold, white, sans-serif font with drop shadow"`
- For infographics, specify style: "polished editorial", "technical diagram", or "hand-drawn whiteboard"
- Ask to "compress" or "summarize" complex info into visual formats

### Character Consistency

Supports up to 14 reference images (6 with high fidelity) for "identity locking":
- Explicitly state: "Keep the person's facial features exactly the same as Image 1"
- Can change expression, pose, angle, or scene while maintaining identity
- Works for characters, products, brand assets across multiple images

### Editing & Restoration

Use semantic instructions - no manual masking needed:
- Object removal: "Remove the tourists from the background and fill with matching textures"
- Colorization: "Colorize this manga panel with vibrant anime style palette"
- Seasonal/lighting: "Turn this scene into winter, add snow, change to cold overcast lighting"
- Style swap: "Redraw this in watercolor style"

### Layout Control

Reference images can control composition, not just content:
- Upload sketches/wireframes to define where elements should sit
- Use grid images to force specific layouts (tile-based, sprite sheets)
- Great for turning napkin sketches into polished assets

### Storyboarding

Can generate sequential art with consistent characters:
- Request specific number of images with narrative arc
- Specify that identity/attire must stay consistent but angles/expressions vary
- Ask for "one image at a time" for better quality

## Reference Image Uses

- Background/color changes
- Style transfer
- Character consistency across scenes
- Pose matching
- Image compositing
- Layout/composition control
- Sketch-to-final conversion

## Limitations

- Small text and fine details may be imperfect
- Verify accuracy of diagrams/infographics
- Complex edits may produce artifacts

## Output

Images saved as `YYYYMMDD_HHMMSS.{png|jpg|webp}` in output directory.
