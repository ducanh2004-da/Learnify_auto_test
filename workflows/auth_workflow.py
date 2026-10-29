from pages.auth_page import AuthPage
from api.flows.auth_flow import AuthFlow

class AuthWorkflow:
    def __init__(self, api_url, context, page=None):
        # Khởi tạo API flow với endpoint và context
        self.auth_flow = AuthFlow(api_url=api_url, context=context)
        self.auth_page = AuthPage(page) if page else None

    def e2e_register_login(self, e2e_data):
        """Dùng API để đăng ký và verify user trước khi login trên UI"""
        import time
        timestamp = int(time.time())
        creds = e2e_data["credentials"]
        creds["email"] = f"testuser_{timestamp}@gmail.com"
        creds["first_name"] = f"user{timestamp}"
        creds["last_name"] = "e2e"
        
        email = creds["email"]
        password = creds["password"]
        
        # 1. Gọi API Register
        register_response = self.auth_flow.register(register_data=e2e_data)
        assert register_response.errors is None, f"GraphQL Error on Register: {register_response.errors}"
        
        # 2. Gọi API Verify tài khoản
        verify_response = self.auth_flow.verifyUserByEmail(email)
        assert verify_response.errors is None, f"GraphQL Error on Verify: {verify_response.errors}"
        
        # 3. Gọi API Login kiểm tra token
        login_response = self.auth_flow.login(e2e_data)
        assert login_response.errors is None, f"GraphQL Error on Login: {login_response.errors}"

        self.auth_page.navigate_to_login()
        self.auth_page.login(e2e_data) 
        return True

        