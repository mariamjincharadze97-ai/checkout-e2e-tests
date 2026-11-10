"""End-to-end checkout tests for the Sauce Demo store.

saucedemo.com is a public demo shop built for test-automation practice.
The login details below are the ones published on its login page.

Run:
    pytest                      # headless, desktop
    pytest --headed             # watch the browser
    pytest --device "iPhone 13" # mobile viewport
"""

import re

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com/"
USER = "standard_user"
PASSWORD = "secret_sauce"  # public demo credential shown on the site


@pytest.fixture
def shop(page: Page) -> Page:
    """Open the store and log in as the standard demo user."""
    page.goto(BASE_URL)
    page.get_by_placeholder("Username").fill(USER)
    page.get_by_placeholder("Password").fill(PASSWORD)
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(re.compile(r"inventory\.html"))
    return page


def add_to_cart(page: Page, product: str) -> None:
    card = page.locator(".inventory_item").filter(has_text=product)
    card.get_by_role("button", name="Add to cart").click()


def test_locked_out_user_sees_error(page: Page):
    page.goto(BASE_URL)
    page.get_by_placeholder("Username").fill("locked_out_user")
    page.get_by_placeholder("Password").fill(PASSWORD)
    page.get_by_role("button", name="Login").click()
    expect(page.locator("[data-test='error']")).to_contain_text("locked out")


def test_cart_badge_counts_added_items(shop: Page):
    add_to_cart(shop, "Sauce Labs Backpack")
    add_to_cart(shop, "Sauce Labs Bike Light")
    expect(shop.locator(".shopping_cart_badge")).to_have_text("2")


def test_removing_item_updates_cart(shop: Page):
    add_to_cart(shop, "Sauce Labs Backpack")
    shop.locator(".shopping_cart_link").click()
    shop.get_by_role("button", name="Remove").click()
    expect(shop.locator(".cart_item")).to_have_count(0)
    expect(shop.locator(".shopping_cart_badge")).to_have_count(0)


def test_checkout_requires_customer_details(shop: Page):
    add_to_cart(shop, "Sauce Labs Backpack")
    shop.locator(".shopping_cart_link").click()
    shop.get_by_role("button", name="Checkout").click()
    shop.get_by_role("button", name="Continue").click()
    expect(shop.locator("[data-test='error']")).to_contain_text("First Name is required")


def test_order_total_is_items_plus_tax(shop: Page):
    add_to_cart(shop, "Sauce Labs Backpack")
    add_to_cart(shop, "Sauce Labs Bike Light")
    shop.locator(".shopping_cart_link").click()
    shop.get_by_role("button", name="Checkout").click()
    shop.get_by_placeholder("First Name").fill("Test")
    shop.get_by_placeholder("Last Name").fill("Buyer")
    shop.get_by_placeholder("Zip/Postal Code").fill("10001")
    shop.get_by_role("button", name="Continue").click()

    def amount(selector: str) -> float:
        return float(re.search(r"[\d.]+", shop.locator(selector).inner_text()).group())

    prices = [float(text.lstrip("$")) for text in shop.locator(".inventory_item_price").all_inner_texts()]
    assert amount(".summary_subtotal_label") == pytest.approx(sum(prices))
    assert amount(".summary_total_label") == pytest.approx(sum(prices) + amount(".summary_tax_label"))


def test_full_purchase_shows_confirmation(shop: Page):
    add_to_cart(shop, "Sauce Labs Backpack")
    shop.locator(".shopping_cart_link").click()
    shop.get_by_role("button", name="Checkout").click()
    shop.get_by_placeholder("First Name").fill("Test")
    shop.get_by_placeholder("Last Name").fill("Buyer")
    shop.get_by_placeholder("Zip/Postal Code").fill("10001")
    shop.get_by_role("button", name="Continue").click()
    shop.get_by_role("button", name="Finish").click()
    expect(shop.get_by_role("heading", name="Thank you for your order!")).to_be_visible()
