from playwright.sync_api import sync_playwright, expect
import os
import sys

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Navigate to the app
            print("Navigating to http://127.0.0.1:8000")
            page.goto("http://127.0.0.1:8000")

            # Check title
            expect(page).to_have_title("Social Golfers Problem Solver")
            print("Title verified.")

            # Fill inputs
            # N=4, G=2, S=2, R=1, T=1 is a trivial solvable case
            print("Filling inputs...")
            page.fill("#players", "4")
            page.fill("#groups", "2")
            page.fill("#group-size", "2")
            page.fill("#rounds", "1")
            page.fill("#pairing", "1")

            # Click solve
            print("Clicking solve...")
            page.click("#solve-button")

            # Wait for result
            # The result table should appear in #schedule-table
            print("Waiting for result...")
            result_div = page.locator("#schedule-table")
            expect(result_div).to_be_visible(timeout=20000)
            expect(result_div).to_contain_text("Round 1")
            expect(result_div).to_contain_text("Group 1")
            expect(result_div).to_contain_text("Group 2")

            print("Result verified.")

            # Take screenshot
            os.makedirs("verification", exist_ok=True)
            screenshot_path = "verification/frontend_success.png"
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

        except Exception as e:
            print(f"Test failed: {e}")
            page.screenshot(path="verification/frontend_failure.png")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
