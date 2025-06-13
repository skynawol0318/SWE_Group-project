from ollama import chat
from ollama import ChatResponse
import json # 응답 파싱을 위해 필요할 수 있습니다.

class OllamaRecyclingLLM:
    def __init__(self, model_name: str = "gemma3:4b", temperature: float = 0.7, max_tokens: int = 200):
        """
        Ollama 모델을 사용하여 분리수거 관련 질의응답을 처리하는 LLM 클래스입니다.

        Args:
            model_name (str): 사용할 Ollama 모델의 이름 (예: "gemma3:4b", "llama3").
            temperature (float): 모델의 답변 다양성 조절 (0.0: 보수적, 1.0: 창의적).
            max_tokens (int): 모델이 생성할 최대 토큰(단어) 수.
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        # 분리수거 가이드라인 시스템 메시지 (초기 프롬프트)
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
        """
        Ollama 모델에 메시지를 전달하고 응답을 생성합니다.
        """
        try:
            response: ChatResponse = chat(
                model=self.model_name,
                messages=messages,
                options={"temperature": self.temperature, "num_predict": self.max_tokens}
            )
            return response['message']['content']
        except Exception as e:
            print(f"Ollama 모델 호출 중 오류 발생: {e}")
            # Ollama 서버 연결 오류 등 발생 시 처리
            return "죄송합니다. 현재 분리수거 정보를 가져올 수 없습니다. Ollama 서버가 실행 중인지 확인해주세요."

    def get_recycling_guidance(self, user_query: str) -> str:
        """
        사용자 쿼리에 대한 분리수거 가이드를 Ollama 모델을 통해 생성합니다.

        Args:
            user_query (str): 사용자의 분리수거 관련 질문.

        Returns:
            str: Ollama 모델이 생성한 분리수거 가이드 답변.
        """
        # 시스템 메시지와 사용자 쿼리로 구성된 메시지 리스트
        messages = [
            self.system_message,
            {"role": "user", "content": user_query}
        ]
        return self._generate_ollama_response(messages)

    def run_example(self, query: str):
        """
        분리수거 LLM의 예시 실행을 보여줍니다.
        """
        print(f"\n[사용자 질문]: {query}")
        response = self.get_recycling_guidance(query)
        print(f"[AI 도우미 답변]: {response}")

# --- 메인 실행 블록 ---
if __name__ == "__main__":
    # Ollama 모델 인스턴스 생성
    # gemma2:9b 같은 더 큰 모델을 사용하면 답변 품질이 더 좋을 수 있습니다.
    # 로컬에 'gemma3:4b' 모델이 pull 되어 있어야 합니다: 'ollama pull gemma3:4b'
    # Ollama 서버가 'ollama run gemma3:4b' 등으로 실행 중이어야 합니다.
    recycling_llm = OllamaRecyclingLLM(
        model_name="gemma3:4b", # 사용 가능한 모델로 변경하세요.
        temperature=0.5,       # 답변의 일관성을 위해 온도를 낮춤
        max_tokens=200         # 답변 길이 제한
    )

    print("--- Ollama 분리수거 LLM 예시 시작 ---")

    # 다양한 분리수거 질문으로 테스트
    recycling_llm.run_example("페트병은 어떻게 버려요?")
    recycling_llm.run_example("라면 봉지는 어디에 버려야 하나요?")
    recycling_llm.run_example("깨진 유리컵은 재활용되나요?")
    recycling_llm.run_example("음식물 쓰레기 중 뼈는 어디에 버려요?")
    recycling_llm.run_example("안 쓰는 플라스틱 칫솔은 어떻게 버리나요?")
    recycling_llm.run_example("다 쓴 건전지는 어떻게 처리해요?")
    recycling_llm.run_example("커피 찌꺼기는 일반 쓰레기인가요?")
    recycling_llm.run_example("재활용이 안 되는 물건은 어떤 것들이 있나요?")
    recycling_llm.run_example("형광등은 어떻게 버리나요?")
    recycling_llm.run_example("오염된 비닐 봉지는 어디에 버려야 하나요?")

    print("\n--- Ollama 분리수거 LLM 예시 종료 ---")
