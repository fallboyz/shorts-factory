# 🎬 쇼츠 제작 및 공장 운영 마스터 가이드 (Production Master Guide)

이 문서는 AI 가이드(안티그래비티)와 함께 고품질 지식 쇼츠를 대량 생산하기 위한 **핵심 전략, 상세 지침 및 운영 규칙**을 다룹니다.

---

## 1. 시스템 비전 (Vision)
*   **목표**: 최소한의 개입으로 고품질 지식 쇼츠를 대량 생산하는 '무인 공장' 구축.
*   **핵심 가치**: 신뢰성 있는 음성(Edge-TTS), 역동적 비주얼(FFmpeg), 빈틈없는 자동화.

---

## 2. 8단계 생산 파이프라인 (The 8-Step Pipeline)

1.  **데이터 수집**: 주제 조사 및 핵심 팩트 정리.
2.  **인벤토리 구축**: `main.py buildup` 명령어로 `inventory.json`에 환경 생성.
3.  **AI 대본 작성**: 아래 [3. 대본 작성 지침]을 엄격히 준수하여 작성.
4.  **오디오 생성**: Edge-TTS를 이용하여 성우 수준의 음성 추출 (+35% 배속).
5.  **비주얼 생성**: 3x2 그리드 규격의 AI 이미지를 생성하고 자동 슬라이싱.
6.  **자막 파일(SRT) 생성**: 오디오 길이에 맞춰 0.1초 단위의 자막 자동 생성.
7.  **애니메이션 적용**: 각 장면에 FFmpeg `zoompan` 필터를 적용하여 역동성 부여.
8.  **최종 합성 및 렌더링**: 영상 + 음성 + 자막을 병합하여 9:16 비율로 인코딩.

---

## 3. 상세 대본 작성 지침 (Scripting Rules)

### 🚫 절대 금지 사항 (Hard Constraints)
*   **섹션 마커 금지**: `[Intro]`, `[Body]` 등의 마커를 절대 사용하지 않는다.
*   **특수 부호 금지**: 괄호(`()`) 및 영어 병기를 금지하며, TTS가 읽는 그대로 한글로만 작성한다.

### 💡 지능적 변주 (Intelligent Scripting)
*   **맥락 유지**: 시리즈물(예: TOP 10)의 경우 전체 주제를 인트로에 포함하되, 매번 문장 구조와 어조를 다게 변주한다.
*   **풍부한 분량**: 쇼츠 기준 **30~50초 분량(공백 포함 200자 이상)**을 확보한다.
*   **구체성**: 단순히 "유명하다"가 아닌, 최신 트렌드(팝업, 드라마 촬영지 등)와 구체적인 고유명사를 활용한다.
*   **랜덤 클로징**: 매번 똑같은 멘트 대신 질문, 감탄, 가정 등 다양한 화법으로 구독/좋아요를 유도한다.

### ✍️ 연출을 위한 줄바꿈 (Production Optimization)
*   **강제 줄바꿈**: 쉼표(,), 느낌표(!), 마침표(.) 등 모든 문장 부호 뒤에는 **반드시 엔터(Enter)**를 친다. (TTS의 자연스러운 휴지와 자막 가독성 확보)
*   **한 줄 길이**: 띄어쓰기 포함 **20자 이내**로 작성한다.

---

## 4. 비주얼 생성 표준 (Visual Production Protocol)

### 🖼️ 그리드 아키텍처 (Grid Architecture)
*   **캔버스 비율**: 1:1 (Square)
*   **레이아웃**: **가로 3칸 x 세로 2행 = 총 6개 패널**
*   **개별 타일 비율**: 각 패널은 **9:16 (Tall/Portrait)** 비율이어야 함.

### 🤖 이미지 프롬프트 필수 조건
이미지 생성 시 아래 키워드를 반드시 포함해야 합니다:
1.  `3x2 Grid composed of six 9:16 tall panels`: 개별 타일의 세로 비율 명시.
2.  `No Borders, No Frames, No Gaps`: 경계선 및 여백 제거.
3.  `Seamless contact sheet`: 타일들이 밀착되어 1:1 정사각형을 꽉 채울 것.

---

## 5. 기술적 연출 상세 (Technical Specifications)

### 🎤 음성 전략 (Edge-TTS)
*   **속도**: 정보 전달력과 몰입감을 극대화하는 **+35% 배속** 적용.
*   **보이스**: 기본값 `ko-KR-SunHiNeural` 사용.

### 🎬 영상 효과 (FFmpeg Zoompan)
*   **Ken Burns Effect**: 정지 화면에 서서히 확대/축소되는 줌팬 효과를 적용하여 지루함을 탈피한다.
*   **해상도**: 최종 출력물 1080x1920 (9:16) FHD 규격.

### 📝 자막 스타일 (Subtitle Specs)
*   **폰트**: `assets/fonts/NanumGothicBold.ttf`
*   **스타일**: `Fontname=NanumGothicBold,FontSize=12,Alignment=2,MarginV=45`

---

## 6. 운영 명령어 (Operations)

### 신규 등록 (Buildup)
```powershell
python main.py buildup --topic "주제이름"
```

### 개별 렌더링 (Single Render)
```powershell
python main.py render --id <번호>
```

### 범위 렌더링 (Batch Render)
```powershell
python main.py render --start <시작번호> --end <끝번호>
```

---

## 7. 정기 관리 및 클린업 (Maintenance & Cleanup)

작업이 완료된 후, 디스크 공간을 확보하거나 새로운 프로젝트를 시작하기 위해 `scripts/` 폴더의 클린업용 스크립트를 사용할 수 있습니다.

### 🧹 프로젝트 초기화 (Full Reset)
최종 결과물인 **MP4 영상과 폰트 파일만 남기고** 모든 중간 리소스(스크립트, 음성, 원본 이미지 등)를 삭제하며 인벤토리를 초기화합니다.
```powershell
python scripts/clean_01_all.py
```
*   **삭제되는 항목**: 작성된 대본, 생성된 음성/이미지/자막 파일, 인벤토리(inventory.json) 기록.
*   **유지되는 항목**: 완성된 쇼츠 영상(`data/output/*.mp4`), 프로젝트 폰트.

### 🪒 부분 관리 (Partial Cleanup)
- `python scripts/clean_02_scripts.py`: 대본 파일만 삭제.
- `python scripts/clean_03_audio.py`: 음성 파일만 삭제.
- `python scripts/clean_04_images.py`: 이미지 및 슬라이싱 데이터 삭제.
- `python scripts/clean_05_output.py`: **[주의]** 최종 출력 영상(.mp4)을 모두 삭제.
- `python scripts/clean_06_inventory.py`: 인벤토리 기록만 초기화.
