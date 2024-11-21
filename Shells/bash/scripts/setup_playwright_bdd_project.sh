#!/bin/ 

# Install necessary system dependencies
sudo apt-get install -y libevent-2.1-7 libgstreamer-plugins-bad1.0-0 libflite1 libx264-dev

# Step 1: Install Playwright-BDD and Playwright
npm i -D playwright-bdd @playwright/test

# Step 2: Install Playwright Browsers
npx playwright install

# Step 3: Set up project structure
mkdir -p tests/features tests/steps tests/support

# Step 4: Create feature file
cat <<EOF > tests/features/example.feature
Feature: Example Feature
  Scenario: Visit Playwright website
    Given I open the Playwright homepage
    Then I should see the Playwright title
EOF

# Step 5: Create step definitions file
cat <<EOF > tests/steps/example.steps.ts
import { Given, Then } from 'playwright-bdd';
import { expect } from '@playwright/test';

Given('I open the Playwright homepage', async ({ page }) => {
  await page.goto('https://playwright.dev');
});

Then('I should see the Playwright title', async ({ page }) => {
  await expect(page).toHaveTitle(/Playwright/);
});
EOF

# Step 6: Create world file
cat <<EOF > tests/support/world.ts
import { setWorldConstructor } from 'playwright-bdd';
import { chromium, Page } from '@playwright/test';

class CustomWorld {
  page: Page;

  constructor() {
    this.page is undefined!;
  }

  async openBrowser() {
    const browser = await chromium.launch();
    this.page = await browser.newPage();
  }

  async closeBrowser() {
    await this.page.close();
  }
}

setWorldConstructor(CustomWorld);
EOF

# Step 7: Create a basic test to ensure everything is set up correctly
cat <<EOF > tests/example.spec.ts
import { test, expect } from '@playwright/test';

test('basic test', async ({ page }) => {
  await page.goto('https://playwright.dev/');
  const title = await page.title();
  expect(title).toBe('Playwright');
});
EOF

# Step 8: Run the tests
npx playwright test
