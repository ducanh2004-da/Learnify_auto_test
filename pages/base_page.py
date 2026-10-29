from playwright.sync_api import Page, expect
class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()

    def click_element(self, selector: str):
        self.page.click(selector)

    def wait_for_element_visible(self, selector: str, timeout: int = 5000):
        self.page.wait_for_selector(selector, state='visible', timeout=timeout)

    def enter_text(self, selector: str, text: str):
        self.page.fill(selector, text)

    def check_for_url(self, url: str, timeout: int = 9000):
        self.page.wait_for_url(url, timeout=timeout)
        print(f"URL after navigation: {self.page.url}")

    def expect_title(self, expected_title: str):
        expect(self.page).to_have_title(expected_title)

    def expect_element_visible(self, selector: str):
        expect(self.page.locator(selector)).to_be_visible()

    def expect_element_text(self, expected_text: str, selector: str):
        expect(self.page.locator(selector)).to_have_text(expected_text)

    def expect_element_contain_text(self, expected_text: str, selector: str, timeout: int = 5000):
        expect(self.page.locator(selector)).to_contain_text(expected_text, timeout=timeout)
        

    def get_html5_validation_message(self, selector):
        """
        Lấy nội dung câu thông báo lỗi mặc định của trình duyệt (HTML5 Validation)
        """
        self.page.wait_for_selector(selector, state="visible")
        # Dùng evaluate để chạy mã JS lấy thuộc tính validationMessage của element
        return self.page.locator(selector).evaluate("element => element.validationMessage")

    def click_enter(self, selector: str):
        input_element = self.page.locator(selector)
        input_element.wait_for(state="visible", timeout=5000)
        input_element.press("Enter")

    def scroll_to_element(self, selector: str):
        element = self.page.locator(selector)
        element.wait_for(state="visible", timeout=5000)
        element.scroll_into_view_if_needed()
    
        