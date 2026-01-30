import re
from .step00_utils import setup_logger

logger = setup_logger(__name__)

class SubtitleGenerator:
    @staticmethod
    def vtt_to_srt(vtt_path, srt_path):
        """
        Converts WebVTT file to SRT format.
        """
        try:
            with open(vtt_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Remove VTT header
            content = re.sub(r'^WEBVTT.*\n', '', content)
            content = re.sub(r'^\n+', '', content) # Remove leading newlines

            # Split into blocks
            blocks = content.strip().split('\n\n')
            
            # Parse all blocks first to fix overlaps
            parsed_blocks = []
            
            def parse_time(t_str):
                # 00:00:00.000 or 00:00:00,000
                t_str = t_str.replace(',', '.')
                h, m, s = t_str.split(':')
                return int(h) * 3600000 + int(m) * 60000 + float(s) * 1000

            def format_time(ms):
                ms = int(ms)
                h = ms // 3600000
                ms %= 3600000
                m = ms // 60000
                ms %= 60000
                s = ms // 1000
                ms %= 1000
                return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

            for block in blocks:
                lines = block.strip().split('\n')
                if not lines: continue
                
                timing_line_idx = 0
                for idx, line in enumerate(lines):
                    if "-->" in line:
                        timing_line_idx = idx
                        break
                
                timing_line = lines[timing_line_idx]
                text_lines = lines[timing_line_idx+1:]
                
                start_str, end_str = timing_line.split(' --> ')
                start_ms = parse_time(start_str.strip())
                end_ms = parse_time(end_str.strip())
                
                parsed_blocks.append({
                    'start': start_ms,
                    'end': end_ms,
                    'text': text_lines
                })

            # --- NEW: Merge short segments ---
            merged_blocks = []
            i = 0
            while i < len(parsed_blocks):
                curr = parsed_blocks[i]
                # If current block is shorter than 1.5s and there's a next block
                # merge it into the next one.
                if (curr['end'] - curr['start'] < 1500) and (i + 1 < len(parsed_blocks)):
                    next_blk = parsed_blocks[i+1]
                    # Combine text
                    combined_text = curr['text'] + next_blk['text']
                    # New block starts at current start, ends at next end
                    merged_blocks.append({
                        'start': curr['start'],
                        'end': next_blk['end'],
                        'text': combined_text
                    })
                    i += 2 # Skip the next one as it's merged
                else:
                    merged_blocks.append(curr)
                    i += 1
            
            parsed_blocks = merged_blocks
            # ---------------------------------

            # Fix Overlaps
            # If current.start < prev.end, set prev.end = current.start - 10ms
            for i in range(len(parsed_blocks) - 1):
                curr = parsed_blocks[i]
                next_blk = parsed_blocks[i+1]
                
                if curr['end'] > next_blk['start']:
                    # Overlap detected! Clip current end.
                    # Ensure minimal gap of 10ms to prevent collision
                    curr['end'] = max(curr['start'], next_blk['start'] - 10)

            # Rebuild SRT
            srt_content = []
            for i, blk in enumerate(parsed_blocks):
                t_str = f"{format_time(blk['start'])} --> {format_time(blk['end'])}"
                text_block = "\n".join(blk['text'])
                srt_content.append(f"{i+1}\n{t_str}\n{text_block}")

            final_srt = "\n\n".join(srt_content)
            
            with open(srt_path, 'w', encoding='utf-8') as f:
                f.write(final_srt)
                
            logger.info(f"Converted VTT to SRT: {srt_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to convert VTT to SRT: {e}")
            return False
