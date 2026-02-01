import argparse
import os
import sys
import logging
from src.step01_inventory import InventoryManager
from src.step02_tts import TTSManager
from src.step03_subtitle import SubtitleGenerator
from src.step04_visual import VisualComposer
from src.step00_utils import setup_logger, ensure_dir, get_project_root

logger = setup_logger("ShortsFactory_Main")

def render_item(inventory, composer, data_dir, item_id, voice):
    """
    Renders a single item. Returns True if success, False otherwise.
    This logic is shared by both single and batch rendering.
    """
    item = inventory.get_item(item_id)
    if not item:
        logger.error(f"Item ID {item_id} not found.")
        return False

    logger.info(f"--- Processing Video {item_id}: {item['topic']} ---")
    
    # 1. Check Resources
    script_path = item["script_path"]
    base_name = f"{item['id']:03d}_{item['topic']}"
    source_image_path = os.path.join(data_dir, "images", base_name, "source.png")
    
    if not os.path.exists(script_path):
        logger.error(f"Script file missing: {script_path}")
        return False
        
    if not os.path.exists(source_image_path):
        logger.error(f"Source image missing: {source_image_path}")
        return False

    try:
        # Read Script
        with open(script_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
            
        if not text:
            logger.error("Script is empty.")
            return False

        # 2. TTS Generation
        logger.info(f"Phase 1: TTS Generation for ID {item_id}...")
        tts = TTSManager(voice=voice)
        tts.generate(text, item["audio_path"], item["subtitle_path"])

        # 3. Visual Composition
        logger.info(f"Phase 2: Visual Composition for ID {item_id}...")
        image_dir = os.path.dirname(source_image_path)
        slices = composer.slice_image(source_image_path, image_dir)
        composer.compose_video(slices, item["audio_path"], item["subtitle_path"], item["output_path"])
        
        inventory.update_status(item["id"], "RENDER_DONE")
        logger.info(f"✅ Render Complete! Output: {item['output_path']}")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to render ID {item_id}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="AI Shorts Factory Pipeline (Universal)")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Buildup Command
    parser_buildup = subparsers.add_parser("buildup", help="Create a new project entry")
    parser_buildup.add_argument("--topic", required=True, help="Topic name")

    # Render Command (Single or Batch)
    parser_render = subparsers.add_parser("render", help="Render video(s)")
    parser_render.add_argument("--id", type=int, help="Single ID to render")
    parser_render.add_argument("--start", type=int, help="Start ID for batch rendering")
    parser_render.add_argument("--end", type=int, help="End ID for batch rendering")
    parser_render.add_argument("--voice", default="ko-KR-SunHiNeural", help="Edge-TTS Voice")

    args = parser.parse_args()
    
    root = get_project_root()
    data_dir = os.path.join(root, "data")
    inventory_path = os.path.join(data_dir, "inventory.json")
    inventory = InventoryManager(inventory_path)
    
    if args.command == "buildup":
        item = inventory.add_item(args.topic)
        item_id = item["id"]
        
        ensure_dir(os.path.join(data_dir, "scripts"))
        ensure_dir(os.path.join(data_dir, "images", f"{item_id:03d}_{args.topic}"))
        ensure_dir(os.path.join(data_dir, "audio"))
        ensure_dir(os.path.join(data_dir, "subtitles"))
        ensure_dir(os.path.join(data_dir, "output"))
        
        base_name = f"{item_id:03d}_{args.topic}"
        inventory.update_paths(item_id,
            script_path=os.path.join(data_dir, "scripts", f"{base_name}.txt"),
            audio_path=os.path.join(data_dir, "audio", f"{base_name}.mp3"),
            subtitle_path=os.path.join(data_dir, "subtitles", f"{base_name}.srt"),
            output_path=os.path.join(data_dir, "output", f"{base_name}.mp4")
        )
        print(f"✅ Buildup Complete for ID {item_id}: {args.topic}")

    elif args.command == "render":
        composer = VisualComposer()
        
        if args.id is not None:
            # Single Mode
            render_item(inventory, composer, data_dir, args.id, args.voice)
        elif args.start is not None and args.end is not None:
            # Batch Mode
            logger.info(f"🚀 Starting Batch Render: IDs {args.start} to {args.end}")
            success_count = 0
            fail_count = 0
            for i in range(args.start, args.end + 1):
                if render_item(inventory, composer, data_dir, i, args.voice):
                    success_count += 1
                else:
                    fail_count += 1
            logger.info(f"🏁 Batch Render Finished. Success: {success_count}, Fail: {fail_count}")
        else:
            logger.error("Error: Please provide either --id or both --start and --end.")
            parser_render.print_help()

    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
