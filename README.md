# ASCII AI - 아스키로 생각하는 AI

ASCII AI는 이미지와 텍스트를 ASCII 아트로 변환하고, ASCII 패턴을 생성하며, ASCII 텍스트를 분석하는 웹 애플리케이션입니다.

## 🚀 Vercel 배포

이 프로젝트는 Vercel을 통해 정적 웹사이트로 배포됩니다.

### 배포 방법

1. GitHub에 코드를 푸시합니다
2. [Vercel](https://vercel.com)에 로그인합니다
3. "New Project"를 클릭합니다
4. GitHub 저장소를 선택합니다
5. 자동으로 배포됩니다

### 프로젝트 구조

```
ASCII/
├── index.html          # 메인 HTML 파일
├── css/
│   └── style.css      # 스타일시트
├── js/
│   └── app.js         # JavaScript 로직
├── images/             # 이미지 파일들
├── vercel.json         # Vercel 배포 설정
└── README.md           # 프로젝트 설명
```

## ✨ 주요 기능

- 🖼️ **이미지를 ASCII로 변환**: 다양한 스타일과 너비로 이미지를 ASCII 아트로 변환
- 📝 **텍스트를 ASCII 아트로**: 입력한 텍스트를 ASCII 아트로 생성
- 🎨 **ASCII 패턴 생성기**: 랜덤, 기하학적, 프랙탈 패턴 생성
- 🔍 **ASCII 분석**: ASCII 텍스트의 통계 및 복잡도 분석

## 🎨 스타일 옵션

### 이미지 변환 스타일
- 표준 (Standard)
- 상세 (Detailed)
- 블록 (Blocks)
- 미니멀 (Minimal)

### 텍스트 아트 스타일
- 블록 (Block)
- 배너 (Banner)
- 심플 (Simple)

### 패턴 유형
- 랜덤 (Random)
- 기하학적 (Geometric)
- 프랙탈 (Fractal)

## ⌨️ 키보드 단축키

- `Ctrl/Cmd + 1`: 이미지 업로드
- `Ctrl/Cmd + 2`: 텍스트 입력 포커스
- `Ctrl/Cmd + 3`: 패턴 생성
- `Ctrl/Cmd + 4`: 분석 입력 포커스

## 🌟 특징

- 반응형 디자인
- 실시간 미리보기
- 애니메이션 효과
- 다크 테마
- 모던한 UI/UX

## 🚀 로컬 개발

정적 파일이므로 간단한 HTTP 서버로 실행할 수 있습니다:

```bash
# Python 3
python -m http.server 8000

# Node.js
npx serve .

# PHP
php -S localhost:8000
```

그 후 브라우저에서 `http://localhost:8000`으로 접속하세요.

## �� 라이선스

MIT License
