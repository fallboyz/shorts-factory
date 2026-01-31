import argparse
import os
import sys
from src.step01_inventory import InventoryManager
from src.step02_tts import TTSManager
from src.step03_subtitle import SubtitleGenerator
from src.step04_visual import VisualComposer
from src.step00_utils import setup_logger, ensure_dir, get_project_root

logger = setup_logger("ShortsFactory_Main")

def main():
    parser = argparse.ArgumentParser(description="AI Shorts Factory Pipeline")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Buildup Command
    parser_buildup = subparsers.add_parser("buildup", help="Create a new project entry")
    parser_buildup.add_argument("--topic", required=True, help="Topic name (e.g., Samsung)")

    # Render Command
    parser_render = subparsers.add_parser("render", help="Render video for an entry")
    parser_render.add_argument("--id", type=int, required=True, help="ID of the item to render")
    parser_render.add_argument("--voice", default="ko-KR-SunHiNeural", help="Edge-TTS Voice")

    args = parser.parse_args()
    
    root = get_project_root()
    data_dir = os.path.join(root, "data")
    inventory_path = os.path.join(data_dir, "inventory.json")
    
    inventory = InventoryManager(inventory_path)
    
    if args.command == "buildup":
        # Create Entry
        item = inventory.add_item(args.topic)
        item_id = item["id"]
        
        # Create Directories
        ensure_dir(os.path.join(data_dir, "scripts"))
        ensure_dir(os.path.join(data_dir, "images", f"{item_id:03d}_{args.topic}"))
        ensure_dir(os.path.join(data_dir, "audio"))
        ensure_dir(os.path.join(data_dir, "subtitles"))
        ensure_dir(os.path.join(data_dir, "output"))
        
        # Update paths in inventory
        base_name = f"{item_id:03d}_{args.topic}"
        inventory.update_paths(item_id,
            script_path=os.path.join(data_dir, "scripts", f"{base_name}.txt"),
            audio_path=os.path.join(data_dir, "audio", f"{base_name}.mp3"),
            subtitle_path=os.path.join(data_dir, "subtitles", f"{base_name}.srt"),
            output_path=os.path.join(data_dir, "output", f"{base_name}.mp4")
        )
        
        print(f"✅ Buildup Complete for ID {item_id}: {args.topic}")
        print(f"👉 Please place script in: data/scripts/{base_name}.txt")
        print(f"👉 Please place 1:1 Image in: data/images/{base_name}/source.png")

    elif args.command == "render":
        item = inventory.get_item(args.id)
        if not item:
            logger.error(f"Item ID {args.id} not found.")
            return

        logger.info(f"Starting Render for ID {args.id}: {item['topic']}")
        
        # 1. Check Resources
        script_path = item["script_path"]
        
        # Determine image dir from inventory or logical path
        # In buildup, we set paths. But image_paths is empty list initially.
        # We expect data/images/{folder}/source.png
        # Let's derive folder name from audio_path or just scan.
        # base_name logic from buildup: f"{item_id:03d}_{args.topic}"
        base_name = f"{item['id']:03d}_{item['topic']}"
        source_image_path = os.path.join(data_dir, "images", base_name, "source.png")
        
        if not os.path.exists(script_path):
            logger.error(f"Script file missing: {script_path}")
            return
            
        if not os.path.exists(source_image_path):
            logger.error(f"Source image missing: {source_image_path}")
            return

        # Read Script
        with open(script_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
            
        if not text:
            logger.error("Script is empty.")
            return

        # 2. TTS Generation
        logger.info("Phase 1: TTS Generation...")
        tts = TTSManager(voice=args.voice)
        try:
            # Generate directly to item["subtitle_path"]
            tts.generate(text, item["audio_path"], item["subtitle_path"])
        except Exception as e:
            logger.error(f"TTS Failed: {e}")
            return

        # 4. Visual Composer
        logger.info("Phase 3: Visual Composition...")
        composer = VisualComposer()
        
        try:
            # Slice Image
            image_dir = os.path.dirname(source_image_path)
            slices = composer.slice_image(source_image_path, image_dir)
            
            # Compose
            composer.compose_video(slices, item["audio_path"], item["subtitle_path"], item["output_path"])
            
            inventory.update_status(item["id"], "RENDER_DONE")
            logger.info(f"✅ Render Complete! Output: {item['output_path']}")
            
        except Exception as e:
            logger.error(f"Visual Composition Failed: {e}")
            return

    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        main()
        sys.stdout.flush()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
