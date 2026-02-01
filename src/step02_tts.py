import subprocess
import os
import sys
from .step00_utils import setup_logger

logger = setup_logger(__name__)

class TTSManager:
    def __init__(self, voice="ko-KR-SunHiNeural", rate="+35%"):
        self.voice = voice
        self.rate = rate

    def generate(self, text, output_audio_path, output_subtitle_path):
        """
        Generates MP3 and Subtitle directly using edge-tts CLI.
        We write directly to the final subtitle path to avoid redundant conversion steps.
        """
        cmd = [
            sys.executable,
            "-m", "edge_tts",
            "--text", text,
            "--voice", self.voice,
            "--rate", self.rate,
            "--write-media", output_audio_path,
            "--write-subtitles", output_subtitle_path
        ]
        
        try:
            logger.info(f"Running TTS: {' '.join(cmd)}")
            # Use DEVNULL for stdout and PIPE for stderr to avoid hanging on large outputs
            result = subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')
            logger.info(f"TTS generation successful: {output_audio_path}")
            return output_subtitle_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"TTS generation failed: {e.stderr}")
            raise
