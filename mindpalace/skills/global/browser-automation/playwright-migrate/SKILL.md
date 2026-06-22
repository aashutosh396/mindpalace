---
name: Playwright Migration (Cypress/Selenium)
description: Use when migrating tests from Cypress or Selenium to Playwright ("migrate tests", "convert tests", "switch to playwright", "move from cypress", "replace selenium").
tags: [playwright, migration, cypress, selenium, webdriver, test-conversion, locators, fixtures, page-objects]
source: alirezarezvani/claude-skills
derived_from: engineering-team/playwright-pro/skills/migrate
---

# Playwright Migration (Cypress/Selenium)

File-by-file conversion from Cypress or Selenium to Playwright.

## Steps

1. **Detect source** — `cypress/` or `cypress.config.ts` → Cypress; `selenium`/`webdriver` deps or `.py` with selenium imports → Selenium.

2. **Assess scope** — count files; size approach: small (1-10) sequential, medium (11-30) batch in groups of 5, large (31+) parallel.

3. **Set up Playwright first** if not configured.

4. **Convert per file:**

Cypress → Playwright:
```
cy.visit(url)           → page.goto(url)
cy.get(selector)        → page.locator(selector) / page.getByRole(...)
cy.contains(text)       → page.getByText(text)
cy.click()              → locator.click()
cy.type(text)           → locator.fill(text)
cy.should('be.visible') → expect(locator).toBeVisible()
cy.should('have.text')  → expect(locator).toHaveText(text)
cy.intercept()          → page.route()
cy.wait('@alias')       → page.waitForResponse()
cy.fixture()            → JSON import / test-data file
```
Custom commands → fixtures (`test.extend()`); plugins → config/fixtures; before/beforeEach → `test.beforeAll()`/`test.beforeEach()`.

Selenium → Playwright:
```
driver.get(url)                    → page.goto(url)
driver.findElement(By.id('x'))     → page.locator('#x') / getByTestId
driver.findElement(By.css('.x'))   → page.locator('.x') / getByRole
element.click()                    → locator.click()
element.sendKeys(text)             → locator.fill(text)
element.getText()                  → locator.textContent()
WebDriverWait + ExpectedConditions → expect(locator).toBeVisible()
driver.switchTo().frame()          → page.frameLocator()
Actions                            → locator.hover() / locator.dragTo()
```
Page objects: keep structure, update API.

5. **Upgrade locators during conversion** — `#id`/`.class`/XPath → getByRole/getByText/getByTestId.

6. **Convert utilities** — custom commands → fixtures; helpers → TS utility functions.

7. **Verify each file** — `npx playwright test <file> --reporter=list`; fix compile/runtime errors before next file.

8. **Clean up** (ask before deleting) — remove old deps + config, update CI to Playwright, update README. Run a coverage check to confirm parity before decommissioning the old suite.

## Output
Conversion summary, tests needing manual intervention, updated CI, before/after run comparison.
