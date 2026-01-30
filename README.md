# Shorts Factory - Michelin Guide Series

AI-powered short-form video generation factory for the Michelin Guide Seoul 2025/2026 series.

## Features
- **Automated Workflow**: From script generation to final video rendering.
- **AI Image Generation**: Context-aware image generation based on Michelin guide data.
- **TTS & Subtitles**: High-quality voice synthesis using Edge TTS and synchronized subtitle generation.
- **Smart Formatting**: Automatic subtitle merging for better readability.

## Directory Structure
- `src/`: Core Python logic for inventory management, TTS, subtitles, and visual assembly.
- `data/`: Placeholder for scripts, images, audio, and output files (Git-ignored).
- `assets/`: Project assets such as fonts.

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Prepare inventory: `inventory.json`
3. Run rendering: `python main.py render --id <ID>`
