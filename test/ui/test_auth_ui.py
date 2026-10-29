import pytest
import allure
from utils.json_reader import load_json_data

LOGIN_DATA = load_json_data("testData_login.json")
HAPPY_LOGIN_PATH = LOGIN_DATA["happy_path"]
UNHAPPY_LOGIN_PATH = LOGIN_DATA["unhappy_path"]
REGISTER_DATA = load_json_data("testData_register.json")
HAPPY_REGISTER_PATH = REGISTER_DATA["happy_path"]
UNHAPPY_REGISTER_PATH = REGISTER_DATA["unhappy_path"]

class TestAuthUI:

    @allure.epic("Xác thực người dùng (Authentication)")
    @allure.feature("Đăng nhập")
    @allure.story("Đăng nhập thành công với tài khoản hợp lệ")
    @allure.title("Kiểm thử đăng nhập thành công với tài khoản hợp lệ")
    @pytest.mark.tc_successful_login
    @pytest.mark.parametrize("login_data", HAPPY_LOGIN_PATH, ids=[item["test_name"] for item in HAPPY_LOGIN_PATH])
    def test_successful_login(self, auth_page, login_data):
        with allure.step("1. Điều hướng đến trang đăng nhập"):
            auth_page.navigate_to_login()
        with allure.step("2. Thực hiện đăng nhập và kiểm tra kết quả điều hướng"):
            auth_page.login(login_data)

    @allure.epic("Xác thực người dùng (Authentication)")
    @allure.feature("Đăng nhập")
    @allure.story("Đăng nhập không thành công")
    @allure.title("Kiểm thử đăng nhập thất bại với thông tin không hợp lệ hoặc để trống")
    @pytest.mark.tc_unsuccessful_login
    @pytest.mark.parametrize("login_data", UNHAPPY_LOGIN_PATH, ids=[item["test_name"] for item in UNHAPPY_LOGIN_PATH])
    def test_unsuccessful_login(self, auth_page, login_data):
        with allure.step("1. Điều hướng đến trang đăng nhập"):
            auth_page.navigate_to_login()
        with allure.step("2. Xác định loại kiểm thử (để trống hoặc sai thông tin)"):
            is_empty_fields = False
            is_unhappy_path = True
            if login_data["test_name"] == "Login with empty email and password fields":
                is_empty_fields = True
                is_unhappy_path = False
        with allure.step("3. Thực hiện đăng nhập và xác thực thông báo lỗi hiển thị"):
            auth_page.login(login_data, is_unhappy_path=is_unhappy_path, is_empty_fields=is_empty_fields)

    @allure.epic("Xác thực người dùng (Authentication)")
    @allure.feature("Đăng ký")
    @allure.story("Đăng ký tài khoản thành công")
    @allure.title("Kiểm thử đăng ký tài khoản thành công với thông tin hợp lệ")
    @pytest.mark.tc_successful_register
    @pytest.mark.parametrize("register_data", HAPPY_REGISTER_PATH, ids=[item["test_name"] for item in HAPPY_REGISTER_PATH])
    def test_successful_register(self, auth_page, register_data):
        with allure.step("1. Điều hướng đến trang đăng ký"):
            auth_page.navigate_to_register()
        with allure.step("2. Thực hiện điền form đăng ký và xác thực thông báo thành công"):
            auth_page.register(register_data)

    @allure.epic("Xác thực người dùng (Authentication)")
    @allure.feature("Đăng ký")
    @allure.story("Đăng ký tài khoản không thành công")
    @allure.title("Kiểm thử đăng ký thất bại khi thông tin không hợp lệ hoặc để trống")
    @pytest.mark.tc_unsuccessful_register
    @pytest.mark.parametrize("register_data", UNHAPPY_REGISTER_PATH, ids=[item["test_name"] for item in UNHAPPY_REGISTER_PATH])
    def test_unsuccessful_register(self, auth_page, register_data):
        with allure.step("1. Điều hướng đến trang đăng ký"):
            auth_page.navigate_to_register()
        with allure.step("2. Kiểm tra các điều kiện xác thực (HTML5 Validation / để trống)"):
            is_html5 = register_data["expected_ui_response"].get("isHtml5Validation", False)
            is_empty = "empty fields" in register_data["test_name"].lower()
        with allure.step("3. Thực hiện gửi form đăng ký và xác thực thông báo lỗi tương ứng"):
            auth_page.register(
                register_data, 
                is_unhappy_path=True, 
                is_empty_fields=is_empty, 
                is_html5_validation=is_html5
            )

        
