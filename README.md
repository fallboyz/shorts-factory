# AI Shorts Factory 🚀

안티그래비티(AI)와 로컬 인프라를 활용한 지식 전달용 쇼츠 자동 생산 공장입니다.

## 📖 문서 가이드
원하시는 목적에 따라 아래 문서를 참고해 주세요.

1.  **[설치 및 환경 구축 가이드 (SETUP_GUIDE.md)](./SETUP_GUIDE.md)**
    *   Python 가상환경 설정, FFmpeg 설치 및 프로젝트 초기화 방법이 담겨 있습니다.
2.  **[쇼츠 제작 및 운영 가이드 (PRODUCTION_GUIDE.md)](./PRODUCTION_GUIDE.md)**
    *   실제 영상을 기획하고 `main.py`를 통해 대량 생산하는 상세 프로세스가 담겨 있습니다.

---

## 🛠️ 핵심 기능
*   **통합 렌더링 시스템**: 단일 테스트부터 대량 배치(Batch) 생산까지 `main.py` 하나로 해결.
*   **고품질 TTS & 자막**: Edge-TTS 기반의 자연스러운 음성과 최적화된 자막 배치.
*   **역동적 비주얼**: FFmpeg Zoompan 효과를 이용한 생동감 넘치는 연출.

---

## 🤖 AI 가이드와 함께 작업하기 (AI Collaboration Example)

이 프로젝트는 **안티그래비티(AI)**와 협업할 때 가장 강력합니다. 아래는 실제 작업 예시입니다.

### 1️⃣ 유저의 요청 (Prompt)
> "2025년 한국인이 가장 많이 방문한 도시 1위 '도쿄'를 주제로 쇼츠 하나 만들어줘."

### 2️⃣ 안티그래비티의 자동 작업
안티그래비티는 `PRODUCTION_GUIDE.md`를 참고하여 다음 과정을 스스로 수행합니다:
1.  **데이터 빌드업**: `python main.py buildup --topic "인기 도시 1위 도쿄"` 실행.
2.  **대본 작성**: 규칙(줄바꿈, 분량 등)에 맞는 대본을 `data/scripts/`에 생성.
3.  **이미지 생성**: `3x2 그리드` 규격의 AI 이미지를 생성하여 프로젝트 폴더에 배치.
4.  **렌더링 실행**: `python main.py render --id <번호>` 명령어로 최종 영상 제작.

### 3️⃣ 결과물 확인
유저님은 `data/output/` 폴더에서 완성된 고화질 쇼츠 영상을 바로 확인하실 수 있습니다.

### 4️⃣ 프로젝트 정리 (Cleanup)
> "작업 끝났어. 결과물만 남기고 다 정리해줘."

안티그래비티는 즉시 `scripts/clean_01_all.py`를 실행하여, **완성된 MP4 영상만 안전하게 보관**하고 용량을 차지하는 중간 작업 파일들을 모두 삭제하여 공장을 깨끗하게 비웁니다.

---

## 🚀 빠른 시작 (Quick Start)
```powershell
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 렌더링 실행 (예: 1번 영상)
python main.py render --id 1

# 3. 프로젝트 초기화 (결과물만 남기고 정리)
python scripts/clean_01_all.py
```

---

## 👤 Author
*   **coulson** ([fallboyz@umount.net](mailto:fallboyz@umount.net))
*   **Blog**: [https://umount.net](https://umount.net)

## 📄 License
이 프로젝트는 **MIT License**를 따릅니다. 자세한 내용은 [LICENSE](./LICENSE) 파일을 확인해 주세요.
