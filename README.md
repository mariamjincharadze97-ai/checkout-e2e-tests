# Checkout end-to-end tests

![tests](https://github.com/mariamjincharadze97-ai/checkout-e2e-tests/actions/workflows/tests.yml/badge.svg)

Automated browser tests for an online store's purchase flow, written with Python, pytest and Playwright.

They run against [saucedemo.com](https://www.saucedemo.com), a public demo shop built for test-automation practice, so this is a demo project. The same structure applies to a real store: log in, fill the cart, check out, verify the numbers.

## What is covered

| Test | What it checks |
|---|---|
| Locked-out user | A blocked account sees a clear error instead of logging in |
| Cart badge | The cart counter matches the number of items added |
| Remove item | Removing a product empties the cart and clears the badge |
| Required fields | Checkout cannot continue without customer details |
| Order total | Subtotal equals the sum of item prices, and total equals subtotal plus tax |
| Full purchase | A complete order ends on the confirmation page |

## Run it

```bash
pip install -r requirements.txt
playwright install chromium

pytest                       # headless, desktop
pytest --headed              # watch the browser
pytest --device "iPhone 13"  # mobile viewport
```

## Continuous integration

Every push runs the suite on GitHub Actions on desktop and on a mobile viewport. On failure, Playwright traces are saved as a build artifact, so each failed step can be replayed with screenshots.
