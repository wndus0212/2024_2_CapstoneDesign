import openai
import json

# OpenAI API 키 설정
openai.api_key = 'wwww'

# 사용자로부터 프롬프트 입력 받기
user_prompt = input("투자 계획 : ")

# OpenAI API 호출
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": user_prompt}],
    max_tokens=1000  # 응답 길이 조절
)

# API 응답에서 텍스트 추출 및 JSON 파싱
gpt_response = response['choices'][0]['message']['content']

try:
    stock_portfolio = json.loads(gpt_response)

    # 결과 출력
    for stock in stock_portfolio:
        print(f"종목: {stock['name']} ({stock['stock']})")
        print(f"할당 비율: {stock['allocation']}")
        print(f"예상 배당 수익률: {stock['expected_dividend_yield']}")
        print(f"추천 이유: {stock['reason']}")
        print(f"리스크: {stock['risk']}")
        print()

except json.JSONDecodeError:
    print("응답이 올바른 JSON 형식이 아닙니다. 다시 시도해 보세요.")
