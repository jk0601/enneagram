from flask import Flask, render_template, request, session, make_response
import openai
import os
from dotenv import load_dotenv
import re
from datetime import datetime

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

application = Flask(__name__)
application.secret_key = 'enneagram_secret_key_2024'  # 세션 사용을 위한 키
app = application  # AWS Elastic Beanstalk을 위한 설정

def format_result_to_html(result):
    """GPT 결과를 HTML로 포맷팅"""
    # 이모지와 함께 시작하는 섹션들을 감지하고 적절한 CSS 클래스 적용
    sections = [
        (r'\*\*🎯 예상 성격유형:(.*?)\*\*', r'<div class="personality-type">\1</div>'),
        (r'\*\*💡 주요 특징:\*\*(.*?)(?=\*\*|$)', r'<div class="characteristics"><h3>💡 주요 특징</h3>\1</div>'),
        (r'\*\*📈 성장 방향:\*\*(.*?)(?=\*\*|$)', r'<div class="growth-section"><h3>📈 성장 방향</h3>\1</div>'),
        (r'\*\*⚠️ 스트레스 상황:\*\*(.*?)(?=\*\*|$)', r'<div class="stress-section"><h3>⚠️ 스트레스 상황</h3>\1</div>'),
        (r'\*\*🤝 인간관계 스타일:\*\*(.*?)(?=\*\*|$)', r'<div class="relationship-section"><h3>🤝 인간관계 스타일</h3>\1</div>'),
        (r'\*\*💬 한줄 요약:\*\*(.*?)(?=\*\*|$)', r'<div class="summary-section"><h3>💬 한줄 요약</h3>\1</div>'),
        (r'\*\*분석 근거:\*\*(.*?)(?=\*\*|$)', r'<div class="analysis-basis"><h3>🔍 분석 근거</h3>\1</div>')
    ]
    
    formatted_result = result
    for pattern, replacement in sections:
        formatted_result = re.sub(pattern, replacement, formatted_result, flags=re.DOTALL)
    
    # 리스트 아이템 처리 (글머리표 제거)
    # formatted_result = re.sub(r'- (.*?)(?=\n|$)', r'<li>\1</li>', formatted_result)
    # formatted_result = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', formatted_result, flags=re.DOTALL)
    
    # 줄바꿈 처리
    formatted_result = formatted_result.replace('\n', '<br>')
    
    return formatted_result

@app.route('/')
def index():
    return render_template('index.html', question_answers={})

@app.route('/analyze', methods=['POST'])
def analyze():
    # 자기소개 입력 받기
    user_input = request.form.get('description', '')
    
    # 질문지 응답 받기
    questions = []
    missing_questions = []
    question_answers = {}
    
    for i in range(1, 13):  # q1부터 q12까지
        answer = request.form.get(f'q{i}')
        if answer:
            questions.append(f"질문 {i}: {get_question_text(i)} - {get_answer_text(answer)}")
            question_answers[f'q{i}'] = answer
        else:
            missing_questions.append(f"질문 {i}")
    
    # 필수 입력 검증
    if not user_input.strip():
        error_message = "자기소개를 작성해주세요."
        return render_template('index.html', result=error_message, user_input=user_input, question_answers=question_answers)
    
    if missing_questions:
        error_message = f"다음 질문에 답변해주세요: {', '.join(missing_questions)}"
        return render_template('index.html', result=error_message, user_input=user_input, question_answers=question_answers)
    
    # 질문지 응답을 텍스트로 변환
    questionnaire_text = '\n'.join(questions)
    
    # 통합 분석 프롬프트
    prompt = f"""
당신은 전문적인 애니어그램 성격 분석가입니다. 사용자의 자기소개와 질문지 응답을 종합적으로 분석하여 가장 적합한 애니어그램 성격유형을 정확하게 진단해주세요.

【자기소개 내용】
{user_input}

【질문지 응답】
{questionnaire_text}

위의 두 가지 정보를 모두 고려하여 다음 형식으로 종합 분석해주세요:

**🎯 예상 성격유형: ★ [번호] ★ - [유형명]**

**💡 주요 특징:**
자기소개에서 드러난 특징
질문지 응답에서 확인된 특징  
두 분석이 일치하는 핵심 특성

**📈 성장 방향:**
건강한 상태에서 이 유형이 보이는 긍정적 특징과 발전 가능성

**⚠️ 스트레스 상황:**
스트레스를 받을 때 나타나는 부정적 패턴과 주의할 점

**🤝 인간관계 스타일:**
타인과의 관계에서 보이는 행동 패턴과 소통 방식

**💬 한줄 요약:**
이 사람의 본질적 성격을 한 문장으로 표현

**분석 근거:**
자기소개와 질문지 중 어떤 부분이 이 유형 판단의 핵심 근거가 되었는지 간략히 설명

애니어그램 9가지 유형:
1번 완벽주의자 - 완벽을 추구하고 원칙을 중시
2번 조력자 - 남을 돕고 관계를 중시  
3번 성취자 - 성공과 인정을 추구
4번 예술가 - 독특함과 감정의 깊이를 중시
5번 관찰자 - 지식과 독립을 추구
6번 충성가 - 안전과 소속감을 중시
7번 열정가 - 즐거움과 새로운 경험을 추구
8번 지배자 - 힘과 통제를 중시
9번 중재자 - 평화와 조화를 추구
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 애니어그램 분야의 전문가로서, 자기소개와 질문지 응답을 종합적으로 분석하여 정확하고 통찰력 있는 성격 분석을 제공합니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        formatted_result = format_result_to_html(result)
        
        # 세션에 분석 결과 저장 (다운로드용)
        session['analysis_result'] = result
        session['analysis_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return render_template('result.html', result=formatted_result)
    
    except Exception as e:
        error_message = f"분석 중 오류가 발생했습니다: {str(e)}"
        return render_template('index.html', result=error_message, user_input=user_input, question_answers=question_answers)

def get_question_text(num):
    """질문 번호에 따른 질문 텍스트 반환"""
    questions = {
        1: "나는 완벽을 추구하는 편이다",
        2: "나는 다른 사람을 도와야 마음이 편하다",
        3: "나는 남들에게 인정받고 싶어한다",
        4: "나는 감정적이고 예술적 성향이 강하다",
        5: "나는 혼자 있는 시간을 중요하게 여긴다",
        6: "나는 안전하고 확실한 것을 선호한다",
        7: "나는 새로운 경험과 즐거움을 추구한다",
        8: "나는 강하고 독립적인 성격이다",
        9: "나는 평화롭고 조화로운 관계를 중시한다",
        10: "나는 실수를 용납하지 못한다",
        11: "나는 다른 사람의 감정을 잘 알아차린다",
        12: "나는 목표를 달성하는 것이 중요하다"
    }
    return questions.get(num, f"질문 {num}")

def get_answer_text(value):
    """답변 값에 따른 텍스트 반환"""
    answers = {
        '1': '전혀 아니다',
        '2': '아니다', 
        '3': '보통이다',
        '4': '그렇다',
        '5': '매우 그렇다'
    }
    return answers.get(value, value)

@app.route('/download')
def download_result():
    """분석 결과를 HTML 파일로 다운로드"""
    if 'analysis_result' not in session:
        return "다운로드할 분석 결과가 없습니다. 먼저 분석을 진행해주세요.", 404
    
    result = session.get('analysis_result', '')
    analysis_date = session.get('analysis_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # HTML 파일 내용 구성
    formatted_result = format_result_to_html(result)
    
    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>애니어그램 분석 결과</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
            background: #f8f9fa;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
            margin-bottom: 30px;
        }}
        .analysis-info {{
            background: #e8f4f8;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
            font-size: 14px;
            color: #666;
        }}
        .personality-type {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-size: 1.2em;
            font-weight: bold;
            margin: 20px 0;
        }}
        .characteristics, .growth-section, .stress-section, .relationship-section, .summary-section {{
            margin: 25px 0;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #3498db;
        }}
                 .characteristics {{ background: #e8f6f3; border-left-color: #27ae60; }}
         .growth-section {{ background: #fff3e0; border-left-color: #f39c12; }}
         .stress-section {{ background: #ffebee; border-left-color: #e74c3c; }}
         .relationship-section {{ background: #f3e5f5; border-left-color: #9b59b6; }}
         .summary-section {{ background: #e3f2fd; border-left-color: #2196f3; }}
         .analysis-basis {{ background: #f8f9fa; border-left-color: #6c757d; font-size: 0.92em; }}
        h3 {{
            color: #2c3e50;
            margin-top: 0;
            font-size: 1.1em;
        }}
        ul {{ margin: 10px 0; }}
        li {{ margin: 5px 0; }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            font-size: 12px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔮 애니어그램 성격 분석 결과</h1>
        
        <div class="analysis-info">
            <strong>분석일시:</strong> {analysis_date}<br>
            <strong>분석도구:</strong> AI 기반 애니어그램 성격 분석기
        </div>
        
        <div class="result-content">
            {formatted_result}
        </div>
        
        <div class="footer">
            <p>이 분석 결과는 AI를 활용한 참고용 자료입니다.</p>
            <p>보다 정확한 성격 분석을 위해서는 전문가와 상담하시기 바랍니다.</p>
            <p><strong>애니어그램 성격 분석기</strong> | 개인 맞춤형 성격 분석 서비스</p>
        </div>
    </div>
</body>
</html>"""
    
    # 영문 파일명 생성 (인코딩 문제 해결)
    timestamp = analysis_date.replace(':', '-').replace(' ', '_')
    filename = f"enneagram_result_{timestamp}.html"
    
    # 응답 생성
    response = make_response(html_content)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 