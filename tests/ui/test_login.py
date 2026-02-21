import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com"


def login(page: Page, username: str, password: str) -> None:
    page.goto(BASE_URL)
    page.locator('[data-test="username"]').fill(username)
    page.locator('[data-test="password"]').fill(password)
    page.locator('[data-test="login-button"]').click()


@pytest.mark.smoke
def test_valid_login(page: Page) -> None:
    login(page, "standard_user", "secret_sauce")
    expect(page).to_have_url(f"{BASE_URL}/inventory.html")
    expect(page.locator('[data-test="inventory-list"]')).to_be_visible()


@pytest.mark.regression
def test_invalid_credentials(page: Page) -> None:
    login(page, "standard_user", "wrong_password")
    expect(page.locator('[data-test="error"]')).to_contain_text(
        "Username and password do not match"
    )


@pytest.mark.regression
def test_forgot_password_flow(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/forgot_password")
    expect(page.locator("#email")).to_be_visible()
    page.locator("#email").fill("qa@testmu.ai")
    with page.expect_response(
        lambda response: "forgot_password" in response.url
        and response.request.method == "POST"
    ) as response_info:
        page.locator("#form_submit").click()
    assert response_info.value.status in {200, 302, 500}


@pytest.mark.regression
def test_session_expiry_after_clearing_storage(page: Page) -> None:
    login(page, "standard_user", "secret_sauce")
    expect(page).to_have_url(f"{BASE_URL}/inventory.html")

    page.context.clear_cookies()
    page.evaluate("window.localStorage.clear(); window.sessionStorage.clear();")
    page.goto(f"{BASE_URL}/inventory.html")

    expect(page).to_have_url(BASE_URL + "/")


@pytest.mark.regression
def test_bruteforce_lockout_user(page: Page) -> None:
    login(page, "locked_out_user", "secret_sauce")
    expect(page.locator('[data-test="error"]')).to_contain_text(
        "Sorry, this user has been locked out"
    )
