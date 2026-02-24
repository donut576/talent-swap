from django.conf import settings
from .config import SYSTEM_PROMPT

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

class AIAgent:
    def __init__(self):
        if not GENAI_AVAILABLE:
            self.model = None
            self.chat = None
            return
            
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.chat = self.model.start_chat(history=[])
        # 發送系統提示
        self.chat.send_message(SYSTEM_PROMPT)

    def get_response(self, user_input):
        if not GENAI_AVAILABLE or self.chat is None:
            return "抱歉，AI 功能目前無法使用。請聯繫管理員。"
            
        try:
            response = self.chat.send_message(user_input)
            return response.text
        except Exception as e:
            return f"抱歉，發生錯誤：{str(e)}"

    def reset_chat(self):
        if not GENAI_AVAILABLE or self.model is None:
            return
            
        self.chat = self.model.start_chat(history=[])
        # 重新發送系統提示
        self.chat.send_message(SYSTEM_PROMPT)