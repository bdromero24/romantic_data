import { expect, test } from '@playwright/test';

test('renders the Streamlit landing without raw HTML or import errors', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  await expect(page.getByText('ImportError')).toHaveCount(0);
  await expect(page.getByText('render_special_message')).toHaveCount(0);
  await expect(page.getByText('<article class="quote-card">')).toHaveCount(0);
  await expect(page.getByText('<article class="special-message-card">')).toHaveCount(0);
  await expect(page.locator('.stException')).toHaveCount(0);
  await expect(page.locator('.romantic-hero')).toBeVisible();
});
