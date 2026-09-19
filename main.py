import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages import UrbanRoutesPage
import helpers
import data


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        options = Options()
        options.add_argument("--start-maximized")
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        cls.driver = webdriver.Chrome(options=options)

        if helpers.is_url_reachable(data.urban_routes_url):
            cls.driver.get(data.urban_routes_url)
        else:
            raise Exception("URL not reachable")

        cls.page = UrbanRoutesPage(cls.driver)

    def test_set_address(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)

        assert routes_page.get_from_address() == data.address_from
        assert routes_page.get_to_address() == data.address_to

    def test_select_comfort_plan(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.select_comfort_plan()

        assert routes_page.is_comfort_plan_selected()

    def test_fill_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.select_comfort_plan()
        routes_page.enter_phone_number(data.phone_number)

        assert routes_page.is_phone_verified()

    def test_fill_card(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.select_comfort_plan()
        routes_page.enter_payment_method(data.card_number, data.card_code)

        assert routes_page.is_card_linked()

    def test_comment_for_driver(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.select_comfort_plan()
        routes_page.set_message_for_driver(data.message_for_driver)

        assert routes_page.get_message_for_driver() == data.message_for_driver

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.select_comfort_plan()
        routes_page.click_blanket_and_handkerchiefs_slider()

        assert routes_page.is_blanket_and_handkerchiefs_selected()

    def test_order_2_ice_creams(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.select_comfort_plan()
        routes_page.order_ice_cream(2)

        assert routes_page.get_ice_cream_count() == 2

    def test_car_search_and_driver_info(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_route(data.address_from, data.address_to)
        routes_page.select_comfort_plan()
        routes_page.enter_phone_number(data.phone_number)
        routes_page.enter_payment_method(data.card_number, data.card_code)
        routes_page.set_message_for_driver(data.message_for_driver)
        routes_page.click_blanket_and_handkerchiefs_slider()
        routes_page.order_ice_cream(2)
        routes_page.click_order_button()

        assert routes_page.is_car_search_modal_visible()
        assert routes_page.is_driver_info_visible()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()