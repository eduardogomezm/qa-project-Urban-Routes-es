import helpers
import time
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
        self.submit_button = (By.XPATH, "//button[contains(text(),'Call a taxi') or contains(text(),'Pedir un taxi')]")

        # 2. Tarifa / Planes (Corregidos XPaths para Urban Routes)
        self.supportive_plan = (By.XPATH, "//div[contains(@class, 'tcard') and .//div[contains(text(), 'Supportive')]]")
        self.active_tariff = (By.XPATH, "//div[contains(@class, 'tcard') and contains(@class, 'active')]")

        # 3. Teléfono
        self.phone_button = (By.XPATH, "//div[contains(@class, 'np-text') or contains(@class, 'phone')]")
        self.phone_input = (By.ID, "phone")
        self.next_button = (By.XPATH, "//button[contains(text(), 'Next') or contains(text(), 'Siguiente')]")
        self.phone_code_input = (By.ID, "code")
        self.confirm_button = (By.XPATH, "//button[contains(text(), 'Confirm') or contains(text(), 'Confirmar')]")

        # 4. Método de Pago
        self.payment_method_button = (By.CLASS_NAME, "pp-text")
        self.add_card_button = (By.XPATH, "//div[contains(@class, 'pp-row') and .//div[contains(text(), 'Add card') or contains(text(), 'Agregar tarjeta')]]")
        self.card_number_input = (By.ID, "number")
        self.card_code_input = (By.XPATH, "//div[contains(@class, 'card-code-input')]//input[@id='code']")
        self.link_card_button = (By.XPATH, "//button[contains(text(), 'Link') or contains(text(), 'Enlazar')]")
        self.close_payment_modal_button = (By.XPATH, "//div[contains(@class, 'payment-picker')]//button[contains(@class, 'close-button')]")

        # 5. Requisitos de viaje
        self.comment_input = (By.ID, "comment")
        # Switch Manta y Pañuelos
        self.blanket_and_handkerchiefs_slider = (By.XPATH, "//div[contains(@class, 'r-sw-container')]//span[contains(@class, 'slider')]")
        self.blanket_and_handkerchiefs_checkbox = (By.XPATH, "//div[contains(@class, 'r-sw-container')]//input[@type='checkbox']")

        # Contadores de Helado
        self.ice_cream_plus_button = (By.XPATH, "//div[contains(@class, 'r-group-plus')]")
        self.ice_cream_count = (By.XPATH, "//div[contains(@class, 'r-group')]//div[contains(@class, 'counter-value')]")

        # 6. Pedido final
        self.order_button = (By.CLASS_NAME, "smart-button")
        self.car_modal = (By.CLASS_NAME, "order-header-title")

    # --- MÉTODOS DE ACCIÓN (Aseguran que Selenium espere interactividad) ---

    def set_route(self, from_address, to_address):
        self.wait.until(EC.visibility_of_element_located(self.from_field)).send_keys(from_address)
        self.wait.until(EC.visibility_of_element_located(self.to_field)).send_keys(to_address)

    def click_call_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.submit_button)).click()

    def select_supportive_plan(self):
        # Hace scroll si es necesario y espera a que el elemento sea cliqueable
        card = self.wait.until(EC.element_to_be_clickable(self.supportive_plan))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", card)
        card.click()

    def set_comment(self, comment):
        self.wait.until(EC.visibility_of_element_located(self.comment_input)).send_keys(comment)

    def toggle_blanket_and_handkerchiefs(self):
        self.wait.until(EC.element_to_be_clickable(self.blanket_and_handkerchiefs_slider)).click()

    def add_ice_cream(self, count=2):
        plus_btn = self.wait.until(EC.element_to_be_clickable(self.ice_cream_plus_button))
        for _ in range(count):
            plus_btn.click()

        # ========== ADDRESS ==========

    def set_route(self, from_address, to_address):
        from_input = self.wait.until(EC.element_to_be_clickable((By.ID, "from")))
        from_input.clear()
        from_input.send_keys(from_address, Keys.DOWN, Keys.ENTER)
        time.sleep(1)

        to_input = self.wait.until(EC.element_to_be_clickable((By.ID, "to")))
        to_input.clear()
        to_input.send_keys(to_address, Keys.DOWN, Keys.ENTER)
        time.sleep(1)

        try:
            # Localizador flexible compatible con español ("Pedir un taxi") e inglés ("Call a taxi")
            call_btn_xpath = "//button[contains(text(),'Call a taxi') or contains(text(),'Pedir un taxi') or contains(@class, 'button round')]"

            call_btn = self.wait.until(
                EC.presence_of_element_located((By.XPATH, call_btn_xpath))
            )
            # Scroll hasta el elemento y clic asistido por JavaScript
            self.driver.execute_script("arguments[0].scrollIntoView(true);", call_btn)
            self.driver.execute_script("arguments[0].click();", call_btn)
            time.sleep(1)
        except TimeoutException:
            print("[ERROR] 'Call a taxi' button not found or not clickable")
            self.driver.save_screenshot("call_taxi_button_fail.png")
            raise

    def get_from_address(self):
        return self.driver.find_element(By.ID, "from").get_attribute("value")

    def get_to_address(self):
        return self.driver.find_element(By.ID, "to").get_attribute("value")

    # ========== TARIFF PLAN ==========
    def select_supportive_plan(self):
        # Selector XPath específico para la tarjeta del plan Supportive
        supportive_card_xpath = "//div[contains(@class, 'tarriff-card') and .//div[text()='Supportive']]"

        # 1. Esperar a que el elemento esté presente en el DOM
        plan_card = self.wait.until(
            EC.presence_of_element_located((By.XPATH, supportive_card_xpath))
        )

        # 2. Hacer scroll hasta el elemento para asegurar visibilidad
        self.driver.execute_script("arguments[0].scrollIntoView(true);", plan_card)

        # 3. Esperar a que sea clickeable y realizar el clic
        clickable_card = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, supportive_card_xpath))
        )
        clickable_card.click()

    def is_supportive_plan_selected(self):
        active_card = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tcard.active")))
        return "Supportive" in active_card.text

    # ========== NÚMERO DE TELÉFONO ==========
    def enter_phone_number(self, phone_number):
        try:
            np_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "np-button")))
            np_button.click()
        except TimeoutException:
            pass

        phone_input = self.wait.until(EC.element_to_be_clickable((By.ID, "phone")))
        phone_input.clear()
        phone_input.send_keys(phone_number)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))).click()

        code = helpers.retrieve_phone_code(self.driver)
        sms_input = self.wait.until(EC.element_to_be_clickable((By.ID, "code")))
        sms_input.send_keys(code)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))).click()

    def is_phone_verified(self):
        phone_input = self.driver.find_element(By.ID, "phone")
        return phone_input.get_attribute("value") != ""

        # ========== PAGO ==========

    def enter_payment_method(self, card_number, card_code):
        # Haz clic primero en Método de pago.
        try:
            self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "pp-button"))).click()
            time.sleep(1)
        except TimeoutException:
            print("[ERROR] Payment method button not clickable")
            return

        # Espera a que desaparezca la superposición.
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay")))
        except TimeoutException:
            print("[INFO] Overlay still visible after clicking Payment Method")

        # Desplázate hasta el contenedor «Añadir tarjeta».
        try:
            add_card_container = self.driver.find_element(
                By.XPATH,
                "//div[contains(@class, 'pp-title') and text()='Add card']/ancestor::div[contains(@class, 'pp-row')]"
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", add_card_container)
            time.sleep(1)  # Let the DOM update
        except Exception as e:
            print(f"[ERROR] Couldn't find 'Add card' container: {e}")
            return

        # Espera a que esté habilitado.
        try:
            self.wait.until(lambda d: "disabled" not in add_card_container.get_attribute("class"))
            print("[DEBUG] 'Add card' container is now enabled")
        except TimeoutException:
            print("[ERROR] 'Add card' never became enabled")
            self.driver.save_screenshot("add_card_disabled_timeout.png")
            return

        # Haz clic en él.
        try:
            add_card_container.click()
            print("[DEBUG] Clicked 'Add card'")
        except Exception as e:
            print(f"[ERROR] Failed to click 'Add card': {e}")
            self.driver.save_screenshot("add_card_click_fail.png")
            return

        # Rellenar tarjeta
        self.set_card_number(card_number)
        self.set_card_code(card_code)

        # Haz clic en el enlace
        try:
            link_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Link']")))
            link_btn.click()
            print("[DEBUG] Clicked 'Link' button")
        except Exception as e:
            print(f"[ERROR] Failed to click 'Link': {e}")
            self.driver.save_screenshot("link_click_fail.png")

    def set_card_number(self, number):
        try:
            card_input = self.wait.until(EC.visibility_of_element_located((By.ID, "number")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", card_input)
            card_input.clear()
            card_input.send_keys(number)
            card_input.send_keys(Keys.TAB)
            print("[DEBUG] Entered card number and sent TAB")
        except Exception as e:
            print("[ERROR] Failed to set card number:", e)
            self.driver.save_screenshot("card_number_fail.png")

    def set_card_code(self, code):
        try:
            time.sleep(0.5)
            code_input = self.wait.until(EC.visibility_of_element_located((By.ID, "code")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", code_input)
            code_input.clear()
            code_input.send_keys(code)
            code_input.send_keys(Keys.TAB)
            print("[DEBUG] Entered card code and sent TAB")
        except Exception as e:
            print("[ERROR] Failed to set card code:", e)
            self.driver.save_screenshot("card_code_fail.png")

    def is_card_linked(self):
        payment = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pp-button")))
        return "Card" in payment.text

    # ========== COMENTARIO ==========
    def set_message_for_driver(self, message):
        comment_box = self.wait.until(EC.element_to_be_clickable((By.ID, "comment")))
        comment_box.clear()
        comment_box.send_keys(message)

    def get_message_for_driver(self):
        return self.driver.find_element(By.ID, "comment").get_attribute("value")

    # ========== Manta y pañuelos ==========
    def click_blanket_and_handkerchiefs_slider(self):
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "slider"))).click()

    def is_blanket_and_handkerchiefs_selected(self):
        checkbox = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']")))
        return checkbox.get_property("checked")

    # ========== HELADO ==========
    def order_ice_cream(self, count):
        for i in range(count):
            print(f"[DEBUG] Trying to click ice cream button #{i + 1}")
            try:
                button = self.wait.until(EC.element_to_be_clickable((By.ID, "ice-cream")))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                button.click()
                print(f"[DEBUG] Ice cream button #{i + 1} clicked")
            except TimeoutException:
                print(f"[ERROR] Ice cream button not found or not clickable on attempt #{i + 1}")
                self.driver.save_screenshot(f"ice_cream_click_fail_{i + 1}.png")

    def get_ice_cream_count(self):
        try:
            count = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ice-cream-count")))
            return int(count.text)
        except TimeoutException:
            print("[ERROR] Ice cream count element not found.")
            self.driver.save_screenshot("ice_cream_count_fail.png")
            return -1

    # ========== FINAL ORDER ==========
    def click_order_button(self):
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay")))
        except TimeoutException:
            print("[INFO] Overlay still visible before clicking Order")

        try:
            order_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "order")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", order_btn)
            order_btn.click()
            print("[DEBUG] Order button clicked")
        except TimeoutException:
            print("[ERROR] Order button not found or not clickable")
            self.driver.save_screenshot("order_button_fail.png")

    def is_car_search_modal_visible(self):
        try:
            modal = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "order-search")))
            return modal.is_displayed()
        except TimeoutException:
            return False