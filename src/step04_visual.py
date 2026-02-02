import subprocess
import os
import math
from mutagen.mp3 import MP3
from .step00_utils import setup_logger

logger = setup_logger(__name__)

class VisualComposer:
    def __init__(self):
        pass

    def get_audio_duration(self, audio_path):
        audio = MP3(audio_path)
        return audio.info.length

    def slice_image(self, image_path, output_dir):
        """
        Slices a 1024x1024 grid image into six 341x512 images (3 cols, 2 rows).
        """
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        sliced_paths = []
        
        # Grid definition: 3x2
        # Width: 341 (approx), Height: 512
        # We'll use FFmpeg crop
        w = 341
        h = 512
        
        coords = [
            (0, 0), (341, 0), (682, 0),
            (0, 512), (341, 512), (682, 512)
        ]
        
        for idx, (x, y) in enumerate(coords):
            out_name = f"{base_name}_slice_{idx+1}.png"
            out_path = os.path.join(output_dir, out_name)
            
            # crop=w:h:x:y
            cmd = [
                "ffmpeg", "-y", "-nostdin",
                "-i", image_path,
                "-filter:v", f"crop={w}:{h}:{x}:{y}",
                out_path
            ]
            
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                sliced_paths.append(out_path)
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to slice image {idx+1}: {e}")
                raise

        return sliced_paths

    def compose_video(self, image_paths, audio_path, subtitle_path, output_path):
        """
        Creates the final video.
        1. Calculate duration per image.
        2. Create short clips with zoompan.
        3. Concat clips.
        4. Add audio.
        5. Burn subtitles.
        """
        total_duration = self.get_audio_duration(audio_path)
        img_duration = total_duration / len(image_paths)
        
        # Temp dir for clips
        temp_dir = os.path.dirname(output_path)
        clip_paths = []
        
        # 1. Create Clips
        for idx, img_path in enumerate(image_paths):
            clip_name = f"clip_{idx}.mp4"
            clip_path = os.path.join(temp_dir, clip_name)
            
            # Dynamic zoompan: vary direction based on index to reduce monotony
            # Zoom in for even, out for odd, or pan
            # Simple zoom-in effect: z='min(zoom+0.0015,1.5)':d=duration*25:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'
            # Let's keep it simple: Slow zoom in center
            
            # FPS=30
            # duration must be passed to ffmpeg input logic or explicitly set
            
            # Ensure d is enough but not excessively large
            num_frames = int(max(1, img_duration * 60))
            
            cmd = [
                "ffmpeg", "-y", "-nostdin",
                "-loop", "1",
                "-i", img_path,
                # Try lower resolution scaling if 4K is failing
                "-vf", f"scale=1620:2880,zoompan=z='min(zoom+0.0005,1.5)':d={num_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920,format=yuv420p",
                "-c:v", "libx264",
                "-preset", "fast",
                "-t", str(img_duration),
                "-r", "60",
                clip_path
            ]
            
            result = subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')
            if result.returncode != 0:
                logger.error(f"Failed to create clip {idx}: {result.stderr}")
                raise Exception(f"FFmpeg clip creation failed for {img_path}")
            clip_paths.append(clip_path)

        # 2. Concat Clips
        list_file = os.path.join(temp_dir, "clips.txt")
        with open(list_file, "w", encoding='utf-8') as f:
            for p in clip_paths:
                # FFmpeg concat requires forward slashes or escaped backslashes
                safe_path = p.replace("\\", "/")
                f.write(f"file '{safe_path}'\n")
        
        temp_video = os.path.join(temp_dir, "temp_video.mp4")
        result = subprocess.run(["ffmpeg", "-y", "-nostdin", "-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", temp_video], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')
        if result.returncode != 0:
            logger.error(f"Failed to concat clips: {result.stderr}")
            raise Exception("FFmpeg concat failed")

        # 3. Finalize (Audio + Subtitles)
        # FontPath: assets/fonts/NanumGothicBold.ttf
        # Note: libass (ffmpeg subtitles) needs escaped paths.
        
        # Use relative paths for FFmpeg to avoid Windows drive colon headeraches in filters
        # Assuming we are running from project root
        project_root = os.getcwd()
        
        rel_subtitle_path = os.path.relpath(subtitle_path, project_root).replace("\\", "/")
        rel_fonts_dir = os.path.relpath(os.path.join(project_root, "assets", "fonts"), project_root).replace("\\", "/")
        
        # Simplify style: Remove &H colors for now to avoid shell/parsing issues
        # Fontname=NanumGothicBold,FontSize=18,Alignment=2,MarginV=50
        # Adjusted to 45 to compensate for libass low-res scaling behavior.
        # This should place subtitles safely above the Shorts UI bottom overlay.
        style = "Fontname=NanumGothicBold,FontSize=12,Alignment=2,MarginV=45"
        
        cmd_final = [
            "ffmpeg", "-y", "-nostdin",
            "-i", temp_video,
            "-i", audio_path,
            "-filter_complex", f"subtitles='{rel_subtitle_path}':fontsdir='{rel_fonts_dir}':force_style='{style}'",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            output_path
        ]
        
        logger.info(f"Rendering final video: {output_path}")
        result = subprocess.run(cmd_final, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')
        if result.returncode != 0:
            logger.error(f"Final rendering failed: {result.stderr}")
            raise Exception(f"Final rendering failed for {output_path}")
            
        # Cleanup
        if os.path.exists(list_file): os.remove(list_file)
        if os.path.exists(temp_video): os.remove(temp_video)
        for p in clip_paths:
            if os.path.exists(p): os.remove(p)
            
        return output_path
