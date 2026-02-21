import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com"


def login(page: Page, username: str = "standard_user", password: str = "secret_sauce") -> None:
    page.goto(BASE_URL)
    page.locator('[data-test="username"]').fill(username)
    page.locator('[data-test="password"]').fill(password)
    page.locator('[data-test="login-button"]').click()


@pytest.mark.smoke
def test_inventory_widgets_loading(page: Page) -> None:
    login(page)
    items = page.locator('[data-test="inventory-item"]')
    expect(items.first).to_be_visible()
    assert items.count() >= 6


@pytest.mark.regression
def test_dashboard_data_accuracy_and_format(page: Page) -> None:
    login(page)
    names = page.locator('[data-test="inventory-item-name"]').all_text_contents()
    prices = page.locator('[data-test="inventory-item-price"]').all_text_contents()

    assert all(name.strip() for name in names)
    assert all(price.startswith("$") for price in prices)


@pytest.mark.regression
def test_filter_sort_behavior(page: Page) -> None:
    login(page)
    page.locator('[data-test="product-sort-container"]').select_option("lohi")
    prices = page.locator('[data-test="inventory-item-price"]').all_text_contents()
    numeric_prices = [float(p.replace("$", "")) for p in prices]
    assert numeric_prices == sorted(numeric_prices)


@pytest.mark.regression
def test_responsive_layout_mobile(page: Page) -> None:
    page.set_viewport_size({"width": 390, "height": 844})
    login(page)
    expect(page.locator("#react-burger-menu-btn")).to_be_visible()
    expect(page.locator('[data-test="inventory-list"]')).to_be_visible()


@pytest.mark.regression
def test_permission_visibility_locked_out_user(page: Page) -> None:
    login(page, username="locked_out_user")
    expect(page.locator('[data-test="error"]')).to_contain_text("locked out")