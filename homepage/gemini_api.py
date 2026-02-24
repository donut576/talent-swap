from django.conf import settings

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

# 配置 Gemini API
def configure_genai():
    if GENAI_AVAILABLE:
        genai.configure(api_key=settings.GEMINI_API_KEY)

# 初始化聊天模型
def get_chat_model():
    if not GENAI_AVAILABLE:
        return None
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    return chat

# 獲取 AI 回應
def get_ai_response(message):
    if not GENAI_AVAILABLE:
        return "抱歉，AI 功能目前無法使用。請聯繫管理員。"
    
    try:
        chat = get_chat_model()
        if chat is None:
            return "抱歉，AI 功能目前無法使用。"
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        return f"抱歉，發生了一些錯誤：{str(e)}"