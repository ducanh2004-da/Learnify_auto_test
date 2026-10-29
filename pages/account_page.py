from pages.base_page import BasePage
from config.env_config import EnvConfig
from utils.logger import log_info, log_result, log_error
from playwright.sync_api import expect  # Chú ý: import thêm expect trực tiếp từ Playwright

class AccountPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.edit_username_btn = '//button[@aria-label="Edit username"]'
        self.edit_email_btn = '//button[@aria-label="Edit email"]'
        self.edit_phone_number_btn = '//button[@aria-label="Edit phoneNumber"]'

        # Sử dụng ID locator siêu nhanh
        self.edit_username_inp = '#editable-username'
        self.edit_email_inp = '#editable-email'
        self.edit_phone_number_inp = '#editable-phoneNumber'
        self.outside_click_element = 'body'

    def edit_inline_field(self, button_locator, input_locator, new_text):
        """
        Hàm xử lý chung cho mọi trường edit inline trong trang Account.
        Đảm bảo React nhận diện sự thay đổi state.
        """
        # 1. Mở ô edit
        self.click_element(button_locator)
        
        # 2. Đợi input xuất hiện sẵn sàng
        input_element = self.page.locator(input_locator)
        input_element.wait_for(state="visible", timeout=5000)
        
        # 3. Focus, xóa toàn bộ và gõ từng chữ (mô phỏng người thật)
        input_element.click()
        # Dùng clear của Playwright (thường hiệu quả). Nếu vẫn bị cứng đầu, thay bằng Ctrl+A + Backspace
        input_element.clear() 
        input_element.type(new_text, delay=30)
        self.page.wait_for_timeout(1500)
        
        # 4. Kích hoạt lưu
        # Nhấn Enter (dành cho form onKeyDown/onSubmit)
        input_element.press("Enter")
        self.page.wait_for_timeout(1500)

        # VÀ click ra ngoài (dành cho form onBlur)
        self.click_element(self.outside_click_element)
        
        # 5. Đợi thẻ input BIẾN MẤT (Đảm bảo quá trình chuyển đổi UI div -> input -> div đã hoàn tất)
        input_element.wait_for(state="hidden", timeout=5000)

    def edit_information(self, account_data):
        # Lấy dữ liệu test
        new_username = account_data["data"]["username"]
        new_email = account_data["data"]["email"]
        new_phone = account_data["data"]["phoneNumber"]

        # --- 1. Edit Username ---
        self.edit_inline_field(self.edit_username_btn, self.edit_username_inp, new_username)
        # Cách assert cực kỳ mạnh mẽ của Playwright: 
        # Cứ tìm thẻ chứa text đó, nó sẽ tự động retry liên tục trong 5 giây cho đến khi thẻ xuất hiện
        expect(self.page.locator(f'div.editable-field-text:has-text("{new_username}")')).to_be_visible()

        # --- 2. Edit Email ---
        self.edit_inline_field(self.edit_email_btn, self.edit_email_inp, new_email)
        expect(self.page.locator(f'div.editable-field-text:has-text("{new_email}")')).to_be_visible()

        # --- 3. Edit Phone Number ---
        self.edit_inline_field(self.edit_phone_number_btn, self.edit_phone_number_inp, new_phone)
        expect(self.page.locator(f'div.editable-field-text:has-text("{new_phone}")')).to_be_visible()