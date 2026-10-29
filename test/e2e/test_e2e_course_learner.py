import pytest
import allure
from workflows.course_learner_workflow import CourseLearnerWorkflow
from workflows.auth_workflow import AuthWorkflow
from utils.json_reader import load_json_data
from utils.test_context import APIContext
from api.flows.auth_flow import AuthFlow


REGISTER_DATA = load_json_data("testData_register.json")
E2E_REGISTER_LOGIN_PATH = REGISTER_DATA["e2e_register_login"]
COURSE_LEARNER_DATA = load_json_data("testData_learner_course.json")
HAPPY_COURSE_LEARNER_PATH = COURSE_LEARNER_DATA["happy_path"]

@pytest.mark.usefixtures("setup_class")
class TestE2ECourseLearner:
    @pytest.fixture(autouse=True)
    def setup_method(self, page):
        self.context = APIContext() 
        self.auth_workflow = AuthWorkflow(api_url=self.api_url, context=self.context, page=page)
        self.course_learner_workflow = CourseLearnerWorkflow(api_url=self.api_url, context=self.context, page=page)

    @allure.epic("Kiểm thử đầu cuối (E2E)")
    @allure.feature("Quy trình học tập của người học")
    @allure.story("Đăng ký, đăng nhập và tham gia học bài giảng hoàn chỉnh")
    @allure.title("Kiểm thử E2E: Đăng ký, đăng nhập và hoàn thành bài giảng trong khóa học")
    @pytest.mark.tc_e2e_course_learner
    @pytest.mark.parametrize("e2e_auth_data", E2E_REGISTER_LOGIN_PATH, ids=[item["test_name"] for item in E2E_REGISTER_LOGIN_PATH])
    @pytest.mark.parametrize("course_data", HAPPY_COURSE_LEARNER_PATH, ids=[item["test_name"] for item in HAPPY_COURSE_LEARNER_PATH])
    def test_e2e_course_learner(self, auth_page, course_learner_page, e2e_auth_data, course_data):
        with allure.step("1. Đăng ký và chuẩn bị tài khoản người dùng qua API"):
            is_prepared = self.auth_workflow.e2e_register_login(e2e_auth_data)
            assert is_prepared is True, "Quá trình tạo và verify user thất bại!"
        with allure.step("2. Thực hiện luồng truy cập và hoàn thành khóa học"):
            self.course_learner_workflow.e2e_enter_learn_course(course_data)
        
        