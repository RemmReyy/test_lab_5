from playwright.sync_api import sync_playwright, expect, Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = "#user-name"
        self.password_input = "#password"
        self.login_button = "#login-button"

    def navigate(self):
        self.page.goto("https://www.saucedemo.com/")

    def login(self, username: str, password: str):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)


def test_homepage():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.saucedemo.com/")
        expect(page).to_have_title("Swag Labs")
        browser.close()

def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
        browser.close()

def test_login_with_empty_fields():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        page.click('#login-button')
        page.wait_for_selector('div.error-message-container')
        error_msg = page.locator("h3", has_text="Epic sadface: Username is required")
        expect(error_msg).to_be_visible()
        browser.close()

def test_burger_menu():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")
        page.click("#react-burger-menu-btn")
        expect(page.locator(".bm-menu-wrap")).to_have_attribute("aria-hidden", "false")
        browser.close()

def test_product_page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")
        page.click('#item_4_title_link')
        expect(page).to_have_url('https://www.saucedemo.com/inventory-item.html?id=4')

def test_add_to_the_cart():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")
        page.click('#item_4_title_link')
        page.click('#add-to-cart')
        page.goto('https://www.saucedemo.com/cart.html')
        item_name = page.locator(".inventory_item_name")
        expect(item_name).to_have_text("Sauce Labs Backpack")
        browser.close()

def test_remove_from_cart():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")
        page.click('#item_4_title_link')
        page.click('#add-to-cart')
        page.goto('https://www.saucedemo.com/cart.html')
        page.click("#remove-sauce-labs-backpack")
        expect(page.locator(".cart_item")).not_to_be_visible()
        browser.close()

def test_checkout_process():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")
        page.click('#item_4_title_link')
        page.click('#add-to-cart')
        page.goto('https://www.saucedemo.com/cart.html')
        page.click('#checkout')
        page.fill('#first-name', "Name")
        page.fill('#last-name' , "Surname")
        page.fill("#postal-code", "12345")
        page.click('#continue')
        page.click("#finish")
        confirmation_msg = page.locator("h2", has_text="Thank you for your order!")
        expect(confirmation_msg).to_be_visible()
        browser.close()

def test_logout():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("standard_user", "secret_sauce")
        page.click("#react-burger-menu-btn")
        page.click("#logout_sidebar_link")
        expect(page).to_have_url("https://www.saucedemo.com/")
        browser.close()

def test_locked_user_login():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login("locked_out_user", "secret_sauce")
        error_msg = page.locator("h3", has_text="Epic sadface: Sorry, this user has been locked out.")
        expect(error_msg).to_be_visible()
        browser.close()