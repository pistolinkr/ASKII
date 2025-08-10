# ASCII AI - 아스키로 생각하는 AI

OpenAI GPT-4를 사용하여 이미지, 텍스트, 패턴을 ASCII 아트로 변환하고 분석하는 웹 애플리케이션입니다.

## 🚀 주요 기능

- **🖼️ 이미지를 ASCII로 변환**: OpenAI GPT-4가 이미지를 분석하여 아름다운 ASCII 아트 생성
- **📝 텍스트를 ASCII 아트로**: 입력한 텍스트를 다양한 스타일의 ASCII 아트로 변환
- **🎨 ASCII 패턴 생성기**: 랜덤, 기하학적, 프랙탈 패턴 자동 생성
- **🔍 ASCII 분석**: ASCII 아트의 복잡도, 미적 가치, 기술적 특성 분석

## 🛠️ 기술 스택

- **Backend**: Flask (Python)
- **AI**: OpenAI GPT-4 API
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Image Processing**: Pillow (PIL)
- **Styling**: Vercel 스타일의 미니멀한 다크 테마

## 📋 설치 및 설정

### 1. 저장소 클론
```bash
git clone https://github.com/pistolinkr/ASKII.git
cd ASKII
```

### 2. Python 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate     # Windows
```

### 3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. OpenAI API 키 설정
1. [OpenAI API](https://platform.openai.com/api-keys)에서 API 키 발급
2. 프로젝트 루트에 `.env` 파일 생성:
```bash
# .env 파일
OPENAI_API_KEY=your_actual_api_key_here
FLASK_ENV=development
FLASK_DEBUG=1
```

### 5. Flask 서버 실행
```bash
python app.py
```

서버가 `http://localhost:5000`에서 실행됩니다.

## 🌐 API 엔드포인트

### POST `/api/convert-image`
이미지를 ASCII 아트로 변환
```json
{
  "image": "base64_encoded_image",
  "width": 80,
  "style": "standard"
}
```

### POST `/api/generate-text-art`
텍스트를 ASCII 아트로 변환
```json
{
  "text": "ASCII AI",
  "style": "block"
}
```

### POST `/api/generate-pattern`
ASCII 패턴 생성
```json
{
  "patternType": "random",
  "size": 20
}
```

### POST `/api/analyze-ascii`
ASCII 아트 분석
```json
{
  "asciiText": "ASCII art content..."
}
```

## 🎨 사용 방법

1. **이미지 변환**: 이미지 파일을 업로드하고 너비와 스타일을 선택한 후 "ASCII로 변환" 버튼 클릭
2. **텍스트 아트**: 원하는 텍스트를 입력하고 스타일을 선택한 후 "ASCII 아트 생성" 버튼 클릭
3. **패턴 생성**: 패턴 유형과 크기를 선택한 후 "패턴 생성" 버튼 클릭
4. **ASCII 분석**: 분석할 ASCII 텍스트를 입력한 후 "분석하기" 버튼 클릭

## 🔧 환경 변수

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `OPENAI_API_KEY` | OpenAI API 키 | 필수 |
| `FLASK_ENV` | Flask 환경 | development |
| `FLASK_DEBUG` | Flask 디버그 모드 | 1 |

## 📱 반응형 디자인

- 모바일, 태블릿, 데스크톱 모든 기기 지원
- Vercel 스타일의 깔끔하고 미니멀한 UI
- 다크 테마로 눈의 피로도 감소

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 🙏 감사의 말

- [OpenAI](https://openai.com/) - GPT-4 API 제공
- [Flask](https://flask.palletsprojects.com/) - 웹 프레임워크
- [Vercel](https://vercel.com/) - 디자인 영감

## 📞 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 [Issues](https://github.com/pistolinkr/ASKII/issues)에 등록해 주세요.
