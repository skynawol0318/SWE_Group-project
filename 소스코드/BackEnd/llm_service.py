# BackEnd/llm_service.py

from ollama import chat, ChatResponse

class OllamaRecyclingLLM:
    def __init__(self, model_name: str = "gemma3:4b", temperature: float = 0.7, max_tokens: int = 200):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_message = {
            "role": "system",
            "content": (
                "너는 대한민국 분리수거 전문 AI 도우미야. 사용자의 질문에 대해 정확하고 친절하게 답변해줘.\n"
                "다음 지침을 반드시 지켜서 답변을 생성해:\n"
                "1. 질문 내용에 따라 구체적이고 현실적인 분리수거 방법을 알려줘.\n"
                "2. 헷갈리기 쉬운 품목(예: 깨진 유리, 오염된 비닐, 영수증, 음식물 묻은 용기, 스티로폼 등)은 특히 '일반쓰레기'로 분류될 수 있음을 강조해줘.\n"
                "3. 답변은 한국어로 하고, 너무 길지 않게 핵심만 명확히 전달해줘.\n"
                "4. 재활용 가능 여부와 올바른 배출 방법을 명확히 구분해서 설명해줘.\n"
                "5. 강조하고 싶은 부분은 '**굵은 글씨**'로 표시해줘.\n"
                "6. 모르는 질문이거나 애매한 경우, 명확하게 답변하기 어렵다고 말하고 다시 질문해달라고 요청해."
            )
        }

    def _generate_ollama_response(self, messages: list) -> str:
        try:
            response: ChatResponse = chat(
                model=self.model_name,
                messages=messages,
                options={"temperature": self.temperature, "num_predict": self.max_tokens}
            )
            return response["message"]["content"]
        except Exception as e:
            print(f"Ollama 모델 호출 중 오류 발생: {e}")
            return "⚠️ Ollama 서버 호출 실패"

    def get_recycling_guidance(self, category: str) -> str:
        """
        분류된 카테고리를 기반으로 재활용 가이드를 생성합니다.
        """
        prompt = f"{category} 분리배출 방법 알려줘."
        messages = [
            self.system_message,
            {"role": "user", "content": prompt}
        ]
        return self._generate_ollama_response(messages)


# 모듈 레벨에서 한 번만 인스턴스화
_llm = OllamaRecyclingLLM()

def get_guidance_for_category(category: str) -> str:
    """
    app.py 에서 호출할 함수입니다.
    """
    return _llm.get_recycling_guidance(category)
