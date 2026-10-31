import os
import pytest
import allure
from config.env_config import EnvConfig, settings
from pages.auth_page import AuthPage
from pages.dashboard_page import DashboardPage
from pages.account_page import AccountPage
from pages.course_learner_page import CourseLearnerPage
from pages.instructor_page import InstructorPage
from pages.lesson_learner_page import LessonLearnerPage
from api.flows.auth_flow import AuthFlow
from utils.test_context import APIContext


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, pytestconfig):
    """
    Ensure headless mode defaults to True in CI environments, while still
    respecting pytest-playwright CLI flags (e.g., --headed) locally.
    """
    is_ci = os.getenv("CI", "false").lower() == "true"
    headed_flag = pytestconfig.getoption("--headed", default=False)

    if is_ci:
        headless = True
    elif headed_flag:
        headless = False
    else:
        headless = settings.HEADLESS

    return {
        **browser_type_launch_args,
        "headless": headless,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Set a consistent desktop viewport so responsive navigation elements
    render identically in local headed and CI headless runs.
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
    }


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
    env_config = EnvConfig()
    api_url = env_config.config["api_url"]
    cleanup_context = APIContext()  # Tạo context riêng cho quá trình dọn dẹp

    # 2. Khởi tạo AuthFlow và thực hiện login Admin
    auth_flow = AuthFlow(api_url=api_url, context=cleanup_context)

    admin_creds = {
        "email": env_config.config["admin_email"],
        "password": env_config.config["admin_password"],
    }

    try:
        # Gọi login bằng API. Hàm này sẽ tự động set 'accessToken' vào cleanup_context
        auth_flow.login(admin_creds)
    except Exception as e:
        print(f"[CLEANUP ERROR] Lỗi đăng nhập Admin, không thể dọn dẹp: {e}")
        return

    # 3. Thực hiện xóa từng user
    for user_id in created_users:
        try:
            auth_flow.deleteUser(user_id)
            print(f"[CLEANUP SUCCESS] Đã xóa thành công tài khoản: {user_id}")
        except Exception as e:
            print(f"[CLEANUP ERROR] Không thể xóa user {user_id}. Lỗi: {e}")


@pytest.fixture(scope="class")
def setup_class(request):
    env_config = EnvConfig()
    request.cls.base_url = env_config.config["base_url"]
    request.cls.api_url = env_config.config["api_url"]


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Capture failure artifacts if test fails during setup or call phase
    if rep.when in ("setup", "call") and rep.failed:
        page = item.funcargs.get("page")
        if page and not page.is_closed():
            try:
                screenshot_bytes = page.screenshot(full_page=True)
                allure.attach(
                    screenshot_bytes,
                    name=f"Screenshot on Failure ({rep.when})",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as e:
                print(f"[ALLURE ATTACHMENT WARNING] Could not capture screenshot: {e}")

            try:
                allure.attach(
                    page.url,
                    name="Failed Page URL",
                    attachment_type=allure.attachment_type.TEXT,
                )
                allure.attach(
                    page.content(),
                    name="Page Source on Failure",
                    attachment_type=allure.attachment_type.HTML,
                )
            except Exception as e:
                print(f"[ALLURE ATTACHMENT WARNING] Could not capture page source: {e}")
