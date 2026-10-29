from utils.json_reader import load_json_data
import pytest
import allure

LOGIN_DATA = load_json_data("testData_login.json")
HAPPY_LOGIN_PATH = LOGIN_DATA["login_for_other_learner_feature"]

ACCOUNT_DATA = load_json_data("testData_account.json")
HAPPY_ACCOUNT_PATH = ACCOUNT_DATA["happy_path"]

class TestAccountUI:

    @allure.epic("Giao diện người dùng (UI)")
    @allure.feature("Quản lý tài khoản cá nhân")
    @allure.story("Cập nhật thông tin tài khoản thành công")
    @allure.title("Kiểm thử cập nhật thông tin tài khoản người học")
    @pytest.mark.tc_successful_edit_account
    @pytest.mark.parametrize("login_data", HAPPY_LOGIN_PATH, ids=[item["test_name"] for item in HAPPY_LOGIN_PATH])
    @pytest.mark.parametrize("account_data", HAPPY_ACCOUNT_PATH, ids=[item["test_name"] for item in HAPPY_ACCOUNT_PATH])
    def test_successful_edit_account(self, auth_page, dashboard_page, account_page, login_data, account_data):
        with allure.step("1. Điều hướng đến trang đăng nhập"):
            auth_page.navigate_to_login()
        with allure.step("2. Đăng nhập với tài khoản người học"):
            auth_page.login(login_data)
        with allure.step("3. Điều hướng đến trang quản lý tài khoản cá nhân"):
            dashboard_page.navigate_to_account_page()
        with allure.step("4. Chỉnh sửa thông tin tài khoản và xác thực kết quả"):
            account_page.edit_information(account_data=account_data)


        
