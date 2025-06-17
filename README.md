# 애니어그램 성격 분석기

OpenAI GPT를 활용한 애니어그램 성격 유형 분석 웹 애플리케이션입니다.

## 🌟 주요 기능

- **통합 분석**: 자기소개 + 12개 문항 질문지를 통한 정확한 애니어그램 성격 유형 분석
- **상세한 분석 결과**: 성격 특징, 성장 방향, 스트레스 상황, 인간관계 스타일 등 종합 분석
- **교육적 참조 자료**: 9가지 유형 요약, 날개(Wings), 스트레스/성장 방향, 3가지 센터 분류
- **깔끔한 UI**: 실버 그라데이션 고급스러운 디자인
- **별도 결과 페이지**: 분석 결과와 참조 정보를 체계적으로 제공

## 🚀 라이브 데모

[여기에 배포된 사이트 URL이 들어갈 예정]

## 📦 설치 및 실행

### 1. 저장소 클론
```bash
git clone [REPOSITORY_URL]
cd enneagram_app
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정
1. `env_example.txt` 파일을 참고하여 `.env` 파일 생성
2. OpenAI API 키 입력:
```
OPENAI_API_KEY=your_actual_api_key_here
```

### 5. 애플리케이션 실행
```bash
python app.py
```

브라우저에서 `http://localhost:5000` 접속

## 🔑 OpenAI API 키 발급 방법

1. https://platform.openai.com 접속
2. 계정 생성 및 로그인  
3. API Keys 메뉴에서 새 키 생성
4. 생성된 키를 `.env` 파일에 입력

## 📱 사용 방법

1. **자기소개 작성**: 성격, 행동 패턴, 가치관 등을 자유롭게 작성
2. **질문지 응답**: 12개 문항에 5점 척도로 답변
3. **통합 분석 시작**: 버튼 클릭하여 분석 요청
4. **결과 확인**: 별도 페이지에서 상세한 분석 결과와 참조 정보 확인
5. **새로운 분석**: "새로운 분석하기" 버튼으로 재사용

## 🛠 기술 스택

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS
- **AI**: OpenAI GPT-4o
- **배포**: Render
- **UI**: 실버 그라데이션 반응형 디자인

## 🔧 배포 옵션

### Option 1: AWS Elastic Beanstalk (추천)

1. **AWS 계정 생성** 및 로그인
2. **배포 파일 준비**:
   ```bash
   # 배포용 ZIP 파일에 포함할 파일들
   application.py          # AWS용 메인 파일
   requirements.txt        # 패키지 의존성
   runtime.txt            # Python 버전
   .ebextensions/         # AWS 설정 폴더
   templates/             # HTML 템플릿
   static/               # CSS 파일
   ```

3. **Elastic Beanstalk 배포**:
   - AWS Console → Elastic Beanstalk
   - "Create Application" 클릭
   - Platform: Python 선택
   - ZIP 파일 업로드
   - 환경변수 설정: `OPENAI_API_KEY`

4. **URL 확인**: 배포 완료 후 제공되는 URL 접속

### Option 2: Render

1. GitHub에 코드 업로드
2. Render에서 새 Web Service 생성
3. GitHub 저장소 연결
4. 환경변수 `OPENAI_API_KEY` 설정
5. 자동 배포 완료

## 📊 애니어그램 유형

이 애플리케이션은 다음 9가지 애니어그램 유형을 분석합니다:

1. **개혁가** - 완벽주의, 원칙 중시
2. **조력가** - 이타적, 관계 중심
3. **성취자** - 목표지향, 성공 추구
4. **개인주의자** - 감성적, 고유성 추구
5. **조사자** - 관찰적, 지식 추구
6. **충실가** - 안전 추구, 충성심
7. **열정가** - 긍정적, 다양성 추구
8. **도전자** - 강인함, 리더십
9. **평화주의자** - 조화, 평화 추구 