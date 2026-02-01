# 🛠️ Shorts Factory 설치 및 환경 구축 가이드 (Setup Guide)

이 문서는 AI 쇼츠 자동화 공장을 로컬 환경에 설치하고 구동하기 위한 기술적 요구사항과 절차를 다룹니다.

---

## 1. 요구 사항 (Prerequisites)
*   **운영 체제**: Windows 11 (한글 환경 권장)
*   **하드웨어**: NVIDIA GPU (FFmpeg 렌더링 가속용 권장)
*   **필수 소프트웨어**:
    *   [Python 3.10+](https://www.python.org/)
    *   [FFmpeg](https://ffmpeg.org/) (환경 변수 PATH 등록 필수)

---

## 2. 설치 단계 (Installation)

### 1) 저장소 클론 및 이동
```powershell
git clone <repository-url>
cd shorts-factory
```

### 2) 가상환경 구축 및 활성화
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 3) 의존성 라이브러리 설치
```powershell
pip install -r requirements.txt
```

---

## 3. 디렉토리 구조 설명 (Internal Structure)
*   `src/`: 핵심 엔진 (관리, TTS, 자막, 비주얼 등)
*   `data/`: 생산 데이터 (스크립트, 이미지, 음성, 최종 영상 등 - Git 제외)
*   `assets/fonts/`: 자막용 나눔고딕 볼드체 폰트 포함

---

## 4. 환경 확인 (Self-Check)
설치가 완료되었다면 아래 명령어로 FFmpeg이 정상 작동하는지 확인하세요.
```powershell
ffmpeg -version
```
