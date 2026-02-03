import os
import json
import logging
from src.step00_utils import setup_logger

logger = setup_logger("ShortsFactory_Marketing")

class MarketingManager:
    def __init__(self):
        pass

    def generate_metadata(self, script_text, topic):
        """
        AI(안티그래비티)의 마케팅 전략을 주입하여 고품질 메타데이터를 생성합니다.
        """
        # 1. 주제명 정제 (예: '01_타오스_험' -> '타오스 험')
        import re
        clean_topic = re.sub(r'^\d+_', '', topic).replace('_', ' ').strip()
        
        logger.info(f"Generating Premium Marketing Metadata for: {clean_topic}")
        
        # 2. 고품질 해시태그 (설명란용)
        hashtags = [
            "#Shorts", "#쇼츠", f"#{clean_topic.replace(' ', '')}",
            "#미스터리", "#공포", "#지식쇼츠", "#소름", "#미해결사건"
        ]
        
        # 3. 검색 최적화 태그 (검색어 노출용)
        suggested_tags = [
            f"{clean_topic} 원인", f"{clean_topic} 소리", f"{clean_topic} 실체",
            "미스터리", "기괴한 사건", "세계 괴담", "공포 실화", "과학 미스터리", "설명 불가능",
            "무서운 이야기", "지식", "안티그래비티"
        ]
        
        metadata = {
            "title": f"600년째 읽지 못한 저주받은 책? {clean_topic}의 실체 😱" if "보이니치" in clean_topic else f"당신만 몰랐던 {clean_topic}의 소름돋는 실체 😱",
            "description": f"한 번 시작하면 멈출 수 없는 {clean_topic} 이야기!\n이 사건의 진짜 원인은 무엇일까요? 여러분의 생각을 댓글로 남겨주세요. 👇\n\n구독과 좋아요는 미스터리를 파헤치는 큰 힘이 됩니다! ✨\n\n" + " ".join(hashtags),
            "hashtags": hashtags,
            "suggested_tags": ", ".join(suggested_tags)
        }
        
        # 타오스 험 전용 커스텀 (예시)
        if "타오스" in clean_topic:
            metadata["title"] = "아직도 정체를 모르는 기괴한 소리, 타오스 험의 진실 😱"
            metadata["description"] = f"전 세계를 공포에 빠뜨린 의문의 소음 {clean_topic}!\n이 소리를 직접 듣는다면 여러분은 어떤 기분일까요?\n\n구독하고 더 많은 우주의 비밀을 만나보세요! ✨\n\n" + " ".join(hashtags)
        
        return metadata

    def save_metadata(self, metadata, output_path):
        """생성된 메타데이터를 사용자가 복사하기 편한 TXT 형식으로 저장합니다."""
        # .json 확장자를 .txt로 변경
        txt_path = output_path.replace('.json', '.txt')
        
        content = f"""[유튜브 쇼츠 제목]
{metadata['title']}

[영상 설명란]
{metadata['description']}

[유튜브 태그 (복사용)]
{metadata['suggested_tags']}
"""
        try:
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"✅ Marketing TXT saved to: {txt_path}")
            
            # (선택 사항) 기존 JSON이 있다면 삭제하거나 유지. 여기선 사용성을 위해 TXT만 강조.
            return True
        except Exception as e:
            logger.error(f"Failed to save marketing text: {e}")
            return False
