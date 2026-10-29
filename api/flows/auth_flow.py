import requests
import base64
import json
from graphql.mutations import auth
from api.parsers import GraphQLResponse 
from api.flows.base_flow import BaseFlow
from utils.logger import log_info, log_error, log_warning, log_result

class AuthFlow(BaseFlow):
    def __init__(self, api_url, context=None):
        super().__init__(api_url=api_url, context=context)
        self.api_url = api_url

    def login(self, login_data=None, is_error=False, password=None) -> GraphQLResponse:
        mutation = auth.LOGIN_MUTATION
        if isinstance(login_data, dict):
            creds = login_data.get("credentials", login_data)
            email_val = creds.get("email")
            password_val = creds.get("password")
        else:
            email_val = login_data
            if password is not None:
                password_val = password
            elif isinstance(is_error, str):
                password_val = is_error
                is_error = False
            else:
                password_val = ""

        variables = {
            "data": {
                "email": email_val,
                "password": password_val
            }
        }
        log_info(f"Sending login request for {email_val}.")
        response = requests.post(self.api_url, json={'query': mutation, 'variables': variables})
        res_data = response.json()
        if is_error is False:
            access_token = res_data.get("data", {}).get("login", {}).get("accessToken")
            refresh_token = res_data.get("data", {}).get("login", {}).get("refreshToken")
            self.variables.set_variable("accessToken", access_token)
            self.variables.set_variable("refreshToken", refresh_token)
            if access_token:
                try:
                    # Lấy phần Payload (phần thứ 2 của token)
                    payload_part = access_token.split('.')[1]
                    # Thêm dấu '=' vào cuối để padding cho đúng chuẩn Base64 của Python
                    padded_payload = payload_part + '=' * (-len(payload_part) % 4)
                    # Giải mã Base64 và parse JSON
                    decoded_payload = json.loads(base64.urlsafe_b64decode(padded_payload))
                    
                    # Lấy trường sub (user id) và lưu vào context
                    user_id = decoded_payload.get("sub")
                    if user_id:
                        self.variables.set_variable("current_user_id", user_id)
                        log_info(f"Đã trích xuất User ID từ Token: {user_id}")
                except Exception as e:
                    log_error(f"Lỗi khi giải mã Access Token: {e}")
        return GraphQLResponse(**res_data)

    def register(self, register_data=None, password=None, phone_number="", email=None, is_error=False) -> GraphQLResponse:
        mutation = auth.REGISTER_MUTATION
        if isinstance(register_data, dict):
            creds = register_data.get("credentials", register_data)
            username = creds.get("username")
            if not username:
                username = f"{creds.get('first_name', '')}{creds.get('last_name', '')}".lower()
            pwd = creds.get("password")
            mail = creds.get("email")
            phone = creds.get("phoneNumber", creds.get("phone_number", ""))
        else:
            username = register_data
            pwd = password
            phone = phone_number or ""
            mail = email

        variables = {
            "data": {
                "username": username,
                "password": pwd,
                "email": mail,
                "phoneNumber": phone
            }
        }
        
        log_info(f"Sending registration request for {username}")
        response = requests.post(self.api_url, json={'query': mutation, 'variables': variables})
        response_data = response.json()
            
        return GraphQLResponse(**response_data)

    def verifyUserByEmail(self, email) -> GraphQLResponse:
        mutation = auth.VERIFY_USER_BY_EMAIL
        variables = {
            "email": email
        }
        log_info("Sending verify user by email request. ")
        response = requests.post(self.api_url, json={'query': mutation, 'variables': variables})
        verify_data = response.json()
        return GraphQLResponse(**verify_data)

    def deleteUser(self, user_id) -> GraphQLResponse:
        mutation = auth.DELETE_USER_MUTATION
        variables = {
            "id": user_id
        }
        token = self.variables.get_variable("accessToken")
        headers = {}
        if token:
            headers['Authorization'] = f"Bearer {token}"
        log_info("Sending delete user request.")
        response = requests.post(self.api_url, json={'query': mutation, 'variables': variables}, headers=headers)
        delete_data = response.json()
        assert "errors" not in delete_data, f"Delete user failed: {delete_data.get('errors')}"
        return GraphQLResponse(**delete_data)
    