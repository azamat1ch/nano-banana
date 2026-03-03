#!/bin/bash
set -e

REPO="https://raw.githubusercontent.com/azamat1ch/nano-banana/main"

if [ "$1" = "--global" ]; then
  SKILL_DIR="$HOME/.claude/skills/nano-banana"
else
  SKILL_DIR=".claude/skills/nano-banana"
fi

echo "Installing nano-banana skill..."

mkdir -p "$SKILL_DIR/scripts"

curl -sSL "$REPO/SKILL.md" -o "$SKILL_DIR/SKILL.md"
curl -sSL "$REPO/scripts/generate.py" -o "$SKILL_DIR/scripts/generate.py"
chmod +x "$SKILL_DIR/scripts/generate.py"

echo ""
echo "  Installed to $SKILL_DIR"
echo "  Restart Claude Code, then use /nano-banana to generate images."
echo ""
echo "  Requires Python 3.10+ and GEMINI_API_KEY."
echo "  Get a key at: https://aistudio.google.com/apikey"
echo "  Set it in $SKILL_DIR/scripts/.env or as an environment variable."
echo ""
echo "  Dependencies auto-install on first run."
if [ "$1" != "--global" ]; then
  echo "  Use --global to install to ~/.claude/skills/ instead."
fi
