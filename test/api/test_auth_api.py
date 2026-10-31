import pytest
import allure
from config.env_config import EnvConfig
from api.flows.auth_flow import AuthFlow
from utils.test_context import APIContext
from utils.json_reader import load_json_data

LOGIN_DATA = load_json_data("testData_login.json")
HAPPY_LOGIN_PATH = LOGIN_DATA["happy_path"]
UNHAPPY_LOGIN_PATH = LOGIN_DATA["unhappy_path"]
REGISTER_DATA = load_json_data("testData_register.json")
HAPPY_REGISTER_PATH = REGISTER_DATA["happy_path"]
UNHAPPY_REGISTER_PATH = REGISTER_DATA["unhappy_path"]

@pytest.mark.usefixtures("setup_class")
class TestAuthApi: 
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.context = APIContext() 
        self.auth_flow = AuthFlow(api_url=self.api_url, context=self.context)

    @allure.epic("Kiểm thử giao tiếp API (API)")
    @allure.feature("API Đăng nhập")
    @allure.story("Đăng nhập API thành công")
    @allure.title("Kiểm thử API đăng nhập thành công với tài khoản hợp lệ")
    @pytest.mark.tc_successful_login
    @pytest.mark.parametrize("login_data", HAPPY_LOGIN_PATH, ids=[item["test_name"] for item in HAPPY_LOGIN_PATH])
    def test_successful_login(self, login_data):
        with allure.step("1. Gửi request GraphQL đăng nhập"):
            response = self.auth_flow.login(login_data)
        
        with allure.step("2. Xác thực phản hồi không có lỗi GraphQL"):
            assert response.errors is None, f"GraphQL Error: {response.errors}"
        
        with allure.step("3. Xác thực Token truy cập (accessToken và refreshToken) trong phản hồi"):
            login_response = response.data.get("login", {})
            assert login_response.get("accessToken") is not None, "Expected access token, but got None"
            assert login_response.get("refreshToken") is not None, "Expected refresh token, but got None"

    @allure.epic("Kiểm thử giao tiếp API (API)")
    @allure.feature("API Đăng nhập")
    @allure.story("Đăng nhập API không thành công")
    @allure.title("Kiểm thử API đăng nhập thất bại với dữ liệu không hợp lệ hoặc lỗi")
    @pytest.mark.tc_unsuccessful_login
    @pytest.mark.parametrize("login_data", UNHAPPY_LOGIN_PATH, ids=[item["test_name"] for item in UNHAPPY_LOGIN_PATH])
    def test_unsuccessful_login(self, login_data):
        with allure.step("1. Gửi request đăng nhập và xử lý phản hồi"):
            if login_data["expected_api_response"]["isError"] is False:
                response = self.auth_flow.login(login_data)
                assert response.errors is None, f"GraphQL Error: {response.errors}"
            else:
                response = self.auth_flow.login(login_data, is_error=True)
                assert response.errors, f"Must have error in that request"
                return
            
        with allure.step("2. Xác thực cờ success là False và thông báo lỗi chính xác"):
            login_response = response.data.get("login", {})
            assert login_response.get("success") is False, "Expected success to be False"
            expected_message = login_data["expected_api_response"]["message"]
            assert login_response.get("message") == expected_message, f"Expected message '{expected_message}' but got '{login_response.get('message')}'"

    @allure.epic("Kiểm thử giao tiếp API (API)")
    @allure.feature("API Đăng ký")
    @allure.story("Đăng ký tài khoản qua API thành công")
    @allure.title("Kiểm thử API đăng ký tài khoản thành công")
    @pytest.mark.tc_successful_register_api
    @pytest.mark.parametrize("register_data", HAPPY_REGISTER_PATH + REGISTER_DATA.get("api_only_path", []), ids=[item["test_name"] for item in HAPPY_REGISTER_PATH + REGISTER_DATA.get("api_only_path", [])])
    def test_successful_register_api(self, register_data):
        """
        Test API Đăng ký thành công (bao gồm cả Happy Path cơ bản và API Only path có phoneNumber)
        """
        with allure.step("1. Gửi GraphQL mutation đăng ký tài khoản"):
            response = self.auth_flow.register(register_data, is_error=False)
        
        with allure.step("2. Xác thực request không có lỗi GraphQL cú pháp"):
            assert response.errors is None, f"GraphQL Error: {response.errors}"
        
        with allure.step("3. Xác thực phản hồi có success là True và thông báo phù hợp"):
            reg_response = response.data.get("register", {})
            assert reg_response.get("success") is True, f"Expected success to be True, but got {reg_response.get('success')}"
            
            expected_msg = register_data.get("expected_api_response", {}).get("message")
            if expected_msg:
                valid_messages = {
                    expected_msg,
                    "User registered successfully. Check email to verify account",
                    "Tài khoản đang chờ kích hoạt. Hệ thống vừa gửi lại email, vui lòng kiểm tra.",
                }
                assert reg_response.get("message") in valid_messages, f"Expected message '{expected_msg}', but got '{reg_response.get('message')}'"

    @allure.epic("Kiểm thử giao tiếp API (API)")
    @allure.feature("API Đăng ký")
    @allure.story("Đăng ký tài khoản qua API thất bại")
    @allure.title("Kiểm thử API đăng ký thất bại khi dữ liệu không hợp lệ")
    @pytest.mark.tc_unsuccessful_register_api
    @pytest.mark.parametrize("register_data", UNHAPPY_REGISTER_PATH, ids=[item["test_name"] for item in UNHAPPY_REGISTER_PATH])
    def test_unsuccessful_register_api(self, register_data):
        """
        Test API Đăng ký thất bại (Trùng email, Validation lỗi từ backend...)
        """
        with allure.step("1. Kiểm tra loại test case (bỏ qua nếu chỉ dành cho kiểm thử UI)"):
            ui_only_cases = ["[REG-002a]", "[REG-002b]", "[REG-002c]", "[REG-004]"]
            if any(case_id in register_data["test_name"] for case_id in ui_only_cases):
                pytest.skip(f"Test case '{register_data['test_name']}' is strictly for UI validation. Skipping in API tests.")

        with allure.step("2. Gửi GraphQL mutation đăng ký với dữ liệu lỗi"):
            response = self.auth_flow.register(register_data, is_error=True)
            expected_api_res = register_data.get("expected_api_response")
        
        with allure.step("3. Xác thực thông báo lỗi trả về từ hệ thống backend"):
            if expected_api_res:
                expected_msg = expected_api_res.get("message")
                if response.errors:
                    assert expected_msg in str(response.errors), f"Expected error '{expected_msg}' not found in GraphQL errors: {response.errors}"
                else:
                    reg_response = response.data.get("register", {})
                    assert reg_response.get("success") is False, "Expected success to be False"
                    assert reg_response.get("message") == expected_msg, f"Expected message '{expected_msg}', but got '{reg_response.get('message')}'"
            else:
                assert response.errors is not None or response.data.get("register", {}).get("success") is False, "Expected API to fail but it succeeded."