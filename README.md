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

## 🚀 빠른 시작 (Quick Start)
```powershell
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 렌더링 실행 (예: 1번 영상)
python main.py render --id 1
```

---

## 👤 Author
*   **coulson** ([fallboyz@umount.net](mailto:fallboyz@umount.net))
*   **Blog**: [https://umount.net](https://umount.net)

## 📄 License
이 프로젝트는 **MIT License**를 따릅니다. 자세한 내용은 [LICENSE](./LICENSE) 파일을 확인해 주세요.
