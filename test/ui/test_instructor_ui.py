from utils.json_reader import load_json_data
import pytest
import allure

LOGIN_DATA = load_json_data("testData_login.json")
HAPPY_LOGIN_PATH = LOGIN_DATA["login_for_other_instructor_feature"]

CREATE_COURSE_DATA = load_json_data("testData_create_course.json")
HAPPY_CREATE_COURSE_PATH = CREATE_COURSE_DATA["happy_path"]

class TestInstrutorUI:
        
    @allure.epic("Giao diện người dùng (UI)")
    @allure.feature("Giảng viên - Tạo khóa học")
    @allure.story("Tạo khóa học AI thành công")
    @allure.title("Kiểm thử tạo khóa học AI và tải bài giảng thành công")
    @pytest.mark.tc_successful_create_course
    @pytest.mark.parametrize("login_data", HAPPY_LOGIN_PATH, ids=[item["test_name"] for item in HAPPY_LOGIN_PATH])
    @pytest.mark.parametrize("create_course_data", HAPPY_CREATE_COURSE_PATH, ids=[item["test_name"] for item in HAPPY_CREATE_COURSE_PATH])
    def test_successful_create_course(self, auth_page, instructor_page, login_data, create_course_data):
        with allure.step("1. Điều hướng đến trang đăng nhập"):
            auth_page.navigate_to_login()
        with allure.step("2. Đăng nhập với tài khoản giảng viên"):
            auth_page.login(login_data)
        with allure.step("3. Điền thông tin tạo khóa học mới"):
            instructor_page.create_course(create_course_data)
        with allure.step("4. Tải lên tệp tài liệu bài học"):
            instructor_page.upload_file(create_course_data["data"]["file"])
        with allure.step("5. Điền thông tin bài học và tạo bài học AI"):
            instructor_page.fill_lesson_information(create_course_data)
    
    @allure.epic("Giao diện người dùng (UI)")
    @allure.feature("Giảng viên - Quản lý khóa học")
    @allure.story("Xem và quản lý chi tiết khóa học")
    @allure.title("Kiểm thử điều hướng đến trang quản lý khóa học và xem chi tiết bài học")
    @pytest.mark.tc_successful_manage_course
    @pytest.mark.parametrize("login_data", HAPPY_LOGIN_PATH, ids=[item["test_name"] for item in HAPPY_LOGIN_PATH])
    def test_successful_manage_course(self, auth_page, instructor_page, login_data):
        with allure.step("1. Điều hướng đến trang đăng nhập"):
            auth_page.navigate_to_login()
        with allure.step("2. Đăng nhập với tài khoản giảng viên"):
            auth_page.login(login_data)
        with allure.step("3. Điều hướng đến trang quản lý và xem chi tiết bài học trong khóa học"):
            instructor_page.manage_course()