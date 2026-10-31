import pytest
import allure
from workflows.auth_workflow import AuthWorkflow
from utils.json_reader import load_json_data
from utils.test_context import APIContext
from api.flows.auth_flow import AuthFlow


REGISTER_DATA = load_json_data("testData_register.json")
E2E_REGISTER_LOGIN_PATH = REGISTER_DATA["e2e_register_login"]


@pytest.mark.usefixtures("setup_class")
class TestE2EAuth:
    @pytest.fixture(autouse=True)
    def setup_method(self, page):
        self.context = APIContext()
        self.auth_workflow = AuthWorkflow(api_url=self.api_url, context=self.context, page=page)

    @allure.epic("Kiểm thử đầu cuối (E2E)")
    @allure.feature("Xác thực người dùng")
    @allure.story("Đăng ký, xác thực và đăng xuất hoàn chỉnh")
    @allure.title("Kiểm thử E2E: Đăng ký tài khoản, đăng nhập và đăng xuất")
    @pytest.mark.tc_e2e_auth
    @pytest.mark.parametrize("e2e_data", E2E_REGISTER_LOGIN_PATH, ids=[item["test_name"] for item in E2E_REGISTER_LOGIN_PATH])
    def test_e2e_auth(self, auth_page, e2e_data, user_cleanup):
        with allure.step("1. Đăng ký và chuẩn bị tài khoản người dùng qua API"):
            is_prepared = self.auth_workflow.e2e_register_login(e2e_data)
            current_user_id = self.auth_workflow.auth_flow.variables.get_variable("current_user_id")
            assert is_prepared is True, "Quá trình tạo và verify user thất bại!"
            if current_user_id:
                user_cleanup.append(current_user_id)
        with allure.step("2. Thực hiện đăng xuất tài khoản trên giao diện UI"):
            auth_page.logout(e2e_data)
