from pages.instructor_page import InstructorPage
from pages.lesson_learner_page import LessonLearnerPage
import pytest
import allure
from config.env_config import EnvConfig
from pages.auth_page import AuthPage
from pages.dashboard_page import DashboardPage
from pages.account_page import AccountPage
from pages.course_learner_page import CourseLearnerPage
from utils.json_reader import load_json_data
from api.flows.auth_flow import AuthFlow
from utils.test_context import APIContext

@pytest.fixture(scope="function")
def auth_page(page):
    return AuthPage(page)

@pytest.fixture(scope="function")
def dashboard_page(page):
    return DashboardPage(page)

@pytest.fixture(scope="function")
def account_page(page):
    return AccountPage(page)

@pytest.fixture(scope="function")
def course_learner_page(page):
    return CourseLearnerPage(page)

@pytest.fixture(scope="function")
def instructor_page(page):
    return InstructorPage(page)

@pytest.fixture(scope="function")
def lesson_learner_page(page):
    return LessonLearnerPage(page)

@pytest.fixture
def user_cleanup():
    # SETUP: Danh sách chứa các user ID cần xóa
    created_users = []
    
    # YIELD: Tạm dừng để trả list này vào test case, hứng các user_id được tạo ra
    yield created_users
    
    # --- TEARDOWN PHASE: Chạy sau khi test xong ---
    if not created_users:
        return  # Nếu không có user nào được tạo thì bỏ qua

    print(f"\n[CLEANUP] Bắt đầu dọn dẹp {len(created_users)} user rác...")

    # 1. Khởi tạo cấu hình và Context độc lập cho cleanup
    env_config = EnvConfig("dev")  
    api_url = env_config.config["api_url"]
    cleanup_context = APIContext()  # Tạo context riêng cho quá trình dọn dẹp
    
    # 2. Khởi tạo AuthFlow và thực hiện login Admin
    auth_flow = AuthFlow(api_url=api_url, context=cleanup_context)
    
    admin_creds = {
        "email": "masteradmin@gmail.com",  # Thay bằng email admin thật của bạn
        "password": "1234567"      # Thay bằng mật khẩu admin thật của bạn
    }
    
    try:
        # Gọi login bằng API. Hàm này (như bạn cung cấp) sẽ tự động set 'accessToken' vào cleanup_context
        auth_flow.login(admin_creds)
    except Exception as e:
        print(f"[CLEANUP ERROR] Lỗi đăng nhập Admin, không thể dọn dẹp: {e}")
        return
    
    # 4. Thực hiện xóa từng user
    for user_id in created_users:
        try:
            auth_flow.deleteUser(user_id)
            print(f"[CLEANUP SUCCESS] Đã xóa thành công tài khoản: {user_id}")
        except Exception as e:
            print(f"[CLEANUP ERROR] Không thể xóa user {user_id}. Lỗi: {e}")

@pytest.fixture(scope="class")
def setup_class(request):
    env_config = EnvConfig("dev")  
    request.cls.base_url = env_config.config["base_url"]
    request.cls.api_url = env_config.config["api_url"]

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    # Nếu test fail trong quá trình thực thi
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get('page')
        if page:
            screenshot_bytes = page.screenshot()
            allure.attach(
                screenshot_bytes,
                name="Screenshot on Failure",
                attachment_type=allure.attachment_type.PNG
            )