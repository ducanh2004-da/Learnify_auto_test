from utils.test_context import APIContext
class BaseFlow:
    def __init__(self, api_url: str, context: APIContext = None):
        self.api_url = api_url
        # Khởi tạo context nếu chưa có để chia sẻ biến toàn cục
        self.variables = context if context else APIContext()