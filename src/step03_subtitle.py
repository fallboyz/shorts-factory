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

            # Fix Overlaps (User's request: Adjust next start to previous end)
            for i in range(1, len(parsed_blocks)):
                prev = parsed_blocks[i-1]
                curr = parsed_blocks[i]
                
                if curr['start'] < prev['end']:
                    # Overlap detected! Push current start forward to match previous end.
                    curr['start'] = prev['end']

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

    @staticmethod
    def vtt_to_ass(vtt_path, ass_path, font_name="Pretendard Bold"):
        """
        Converts WebVTT file to ASS format with custom line spacing hack.
        """
        try:
            with open(vtt_path, 'r', encoding='utf-8') as f:
                content = f.read()

            content = re.sub(r'^WEBVTT.*\n', '', content)
            content = re.sub(r'^\n+', '', content)
            blocks = content.strip().split('\n\n')
            
            parsed_blocks = []
            
            def parse_time(t_str):
                t_str = t_str.replace(',', '.')
                parts = t_str.split(':')
                if len(parts) == 3:
                    h, m, s = parts
                else:
                    h = 0
                    m, s = parts
                return int(h) * 3600000 + int(m) * 60000 + float(s) * 1000

            def format_ass_time(ms):
                ms = int(ms)
                h = ms // 3600000
                ms %= 3600000
                m = ms // 60000
                ms %= 60000
                s = ms // 1000
                ms %= 1000
                return f"{h:01d}:{m:02d}:{s:02d}.{ms//10:02d}"

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
                parsed_blocks.append({
                    'start': parse_time(start_str.strip()),
                    'end': parse_time(end_str.strip()),
                    'text': " ".join(text_lines) # Join multi-line VTT text into one
                })

            # Merge short segments
            merged = []
            i = 0
            while i < len(parsed_blocks):
                curr = parsed_blocks[i]
                if (curr['end'] - curr['start'] < 1500) and (i + 1 < len(parsed_blocks)):
                    next_blk = parsed_blocks[i+1]
                    merged.append({
                        'start': curr['start'],
                        'end': next_blk['end'],
                        'text': curr['text'] + " " + next_blk['text']
                    })
                    i += 2
                else:
                    merged.append(curr)
                    i += 1
            parsed_blocks = merged

            # Fix Overlaps
            for i in range(1, len(parsed_blocks)):
                if parsed_blocks[i]['start'] < parsed_blocks[i-1]['end']:
                    parsed_blocks[i]['start'] = parsed_blocks[i-1]['end']

            # Generate ASS Content
            header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font_name},85,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,3,1,2,40,40,200,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
            events = []
            for blk in parsed_blocks:
                t_start = format_ass_time(blk['start'])
                t_end = format_ass_time(blk['end'])
                
                # --- Smart Wrap & Line Spacing Hack ---
                raw_text = blk['text'].strip()
                
                # If text is longer than ~22 chars, it likely needs wrapping
                # We'll split it and insert a spacing tag {\fs40}\N{\fs85}
                # This adds a vertical gap defined by the \fs40 newline
                if len(raw_text) > 22:
                    mid = len(raw_text) // 2
                    # Find nearest space to split
                    left_space = raw_text.rfind(' ', 0, mid + 5)
                    right_space = raw_text.find(' ', mid - 5)
                    
                    split_idx = left_space if left_space != -1 else right_space
                    if split_idx != -1:
                        part1 = raw_text[:split_idx]
                        part2 = raw_text[split_idx+1:]
                        # The Hack: \N creates newline. 
                        # {\fs40}\N{\fs85} makes the newline height based on size 40, then restores 85
                        text = f"{part1}\\N{{\\fs40}}\\h{{\\fs85}}{part2}"
                    else:
                        text = raw_text
                else:
                    text = raw_text
                
                events.append(f"Dialogue: 0,{t_start},{t_end},Default,,0,0,0,,{text}")

            with open(ass_path, 'w', encoding='utf-8') as f:
                f.write(header + "\n".join(events))
                
            logger.info(f"Converted VTT to ASS: {ass_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to convert VTT to ASS: {e}")
            return False
