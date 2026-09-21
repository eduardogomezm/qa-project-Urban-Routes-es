import helpers
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # 1. Dirección y Ruta
        self.from_field = (By.ID, "from")
        self.to_field = (By.ID, "to")
        self.submit_button = (By.XPATH, "//button[contains(text(),'Call a taxi') or contains(text(),'Pedir un taxi') or contains(@class, 'button round')]")

        # 2. Tarifa / Planes
        self.comfort_plan = (
            By.XPATH,
            "//div[contains(@class, 'tcard') and .//*[normalize-space()='Comfort']]"
        )

        # 3. Teléfono
        self.phone_button = (By.CLASS_NAME, "np-button")
        self.phone_input = (By.ID, "phone")
        self.next_button = (By.XPATH, "//button[contains(text(), 'Next') or contains(text(), 'Siguiente')]")
        self.phone_code_input = (By.ID, "code")
        self.confirm_button = (By.XPATH, "//button[contains(text(), 'Confirm') or contains(text(), 'Confirmar')]")

        # 4. Método de Pago
        self.payment_method_button = (By.CLASS_NAME, "pp-button")
        self.add_card_container = (
            By.XPATH,
            "//div[contains(@class, 'pp-row') and "
            ".//div[contains(@class, 'pp-title') and normalize-space()='Agregar tarjeta']]"
        )
        self.card_number_input = (By.ID, "number")
        self.card_code_input = (By.XPATH, "//input[@placeholder='12']")
        self.link_card_button = (By.XPATH, "//button[normalize-space()='Agregar']")
        self.overlay = (By.CLASS_NAME, "overlay")

        # 5. Requisitos de viaje
        self.comment_input = (By.ID, "comment")
        self.blanket_and_handkerchiefs_slider = (By.CLASS_NAME, "slider")
        self.blanket_checkbox = (By.XPATH, "//input[@type='checkbox']")
        self.ice_cream_button = (By.ID, "ice-cream")
        self.ice_cream_count = (By.CLASS_NAME, "ice-cream-count")

        # 6. Pedido final
        self.order_button = (By.ID, "order")
        self.car_modal = (By.CLASS_NAME, "order-search")
        self.driver_info = (By.CSS_SELECTOR, ".order-body")

    # ========== DIRECCIÓN Y RUTA ==========
    def set_route(self, from_address, to_address):
        from_input = self.wait.until(EC.element_to_be_clickable(self.from_field))
        from_input.clear()
        from_input.send_keys(from_address, Keys.DOWN, Keys.ENTER)

        to_input = self.wait.until(EC.element_to_be_clickable(self.to_field))
        to_input.clear()
        to_input.send_keys(to_address, Keys.DOWN, Keys.ENTER)

        call_btn = self.wait.until(EC.presence_of_element_located(self.submit_button))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", call_btn)
        self.driver.execute_script("arguments[0].click();", call_btn)

    def get_from_address(self):
        return self.wait.until(EC.visibility_of_element_located(self.from_field)).get_attribute("value")

    def get_to_address(self):
        return self.wait.until(EC.visibility_of_element_located(self.to_field)).get_attribute("value")

    # ========== PLANES Y TARIFAS ==========
    def select_comfort_plan(self):
        plan_card = self.wait.until(EC.presence_of_element_located(self.comfort_plan))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", plan_card)
        clickable_card = self.wait.until(EC.element_to_be_clickable(self.comfort_plan))
        clickable_card.click()

    def is_comfort_plan_selected(self):
        active_card = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".tcard.active"))
        )
        return "Comfort" in active_card.text

    # ========== TELÉFONO ==========
    def enter_phone_number(self, phone_number):
        np_btn = self.wait.until(EC.element_to_be_clickable(self.phone_button))
        np_btn.click()

        phone_in = self.wait.until(EC.element_to_be_clickable(self.phone_input))
        phone_in.clear()
        phone_in.send_keys(phone_number)

        self.wait.until(EC.element_to_be_clickable(self.next_button)).click()

        code = helpers.retrieve_phone_code(self.driver)
        sms_in = self.wait.until(EC.element_to_be_clickable(self.phone_code_input))
        sms_in.send_keys(code)

        self.wait.until(EC.element_to_be_clickable(self.confirm_button)).click()

    def is_phone_verified(self):
        phone_btn = self.wait.until(EC.visibility_of_element_located(self.phone_button))
        return phone_btn.text != "" and phone_btn.text != "Número de teléfono"

    # ========== MÉTODO DE PAGO ==========
    def enter_payment_method(self, card_number, card_code):
        self.wait.until(EC.element_to_be_clickable(self.payment_method_button)).click()
        self.wait.until(EC.invisibility_of_element_located(self.overlay))

        add_card_elem = self.wait.until(EC.presence_of_element_located(self.add_card_container))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", add_card_elem)
        self.wait.until(EC.element_to_be_clickable(self.add_card_container)).click()

        self.set_card_number(card_number)
        self.set_card_code(card_code)

        link_btn = self.wait.until(EC.element_to_be_clickable(self.link_card_button))
        link_btn.click()

    def set_card_number(self, number):
        card_input = self.wait.until(EC.visibility_of_element_located(self.card_number_input))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", card_input)
        card_input.clear()
        card_input.send_keys(number, Keys.TAB)

    def set_card_code(self, code):
        code_input = self.wait.until(EC.visibility_of_element_located(self.card_code_input))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", code_input)
        code_input.clear()
        code_input.send_keys(code, Keys.TAB)

    def is_card_linked(self):
        payment = self.wait.until(EC.presence_of_element_located(self.payment_method_button))
        return "Card" in payment.text or "Tarjeta" in payment.text

    # ========== COMENTARIO PARA EL CONDUCTOR ==========
    def set_message_for_driver(self, message):
        comment_box = self.wait.until(EC.element_to_be_clickable(self.comment_input))
        comment_box.clear()
        comment_box.send_keys(message)

    def get_message_for_driver(self):
        return self.wait.until(EC.visibility_of_element_located(self.comment_input)).get_attribute("value")

    # ========== REQUISITOS ADICIONALES ==========
    def click_blanket_and_handkerchiefs_slider(self):
        self.wait.until(EC.element_to_be_clickable(self.blanket_and_handkerchiefs_slider)).click()

    def is_blanket_and_handkerchiefs_selected(self):
        checkbox = self.wait.until(EC.presence_of_element_located(self.blanket_checkbox))
        return checkbox.get_property("checked")

    def order_ice_cream(self, count):
        for _ in range(count):
            button = self.wait.until(EC.element_to_be_clickable(self.ice_cream_button))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
            button.click()

    def get_ice_cream_count(self):
        count_elem = self.wait.until(EC.visibility_of_element_located(self.ice_cream_count))
        return int(count_elem.text)

    # ========== PEDIDO FINAL ==========
    def click_order_button(self):
        self.wait.until(EC.invisibility_of_element_located(self.overlay))
        order_btn = self.wait.until(EC.element_to_be_clickable(self.order_button))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", order_btn)
        order_btn.click()

    def is_car_search_modal_visible(self):
        try:
            modal = self.wait.until(EC.visibility_of_element_located(self.car_modal))
            return modal.is_displayed()
        except TimeoutException:
            return False

    def is_driver_info_visible(self):
        try:
            driver_info = self.wait.until(
                EC.visibility_of_element_located(self.driver_info)
            )
            return driver_info.is_displayed()
        except TimeoutException:
            return False

    def close_payment_modal(self):
        close_button = (
            By.CSS_SELECTOR,
            ".payment-picker .section.active .section-close"
        )
        self.wait.until(EC.element_to_be_clickable(close_button)).click()
        self.wait.until(EC.invisibility_of_element_located(self.overlay))