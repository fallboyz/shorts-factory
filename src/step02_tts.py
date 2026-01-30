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
        Generates MP3 and VTT (Subtitle) using edge-tts CLI.
        Note: edge-tts outputs subtitles in VTT format by default when using --write-subtitles.
        We will rely on SubtitleGenerator to convert VTT to SRT.
        """
        # We need a temporary VTT path because edge-tts writes to a specific extension
        temp_vtt_path = output_audio_path.replace(".mp3", ".vtt")
        
        cmd = [
            sys.executable,
            "-m", "edge_tts",
            "--text", text,
            "--voice", self.voice,
            "--rate", self.rate,
            "--write-media", output_audio_path,
            "--write-subtitles", temp_vtt_path
        ]
        
        try:
            logger.info(f"Running TTS: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info("TTS generation successful")
            
            # If the user requested a specific subtitle path (which might be used later for VTT->SRT),
            # we just return the path to the generated VTT for now, or move it if needed.
            # For simplicity, we assume the caller will handle the VTT->SRT conversion using the temp_vtt_path.
            return temp_vtt_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"TTS generation failed: {e.stderr}")
            raise
