import { test, expect } from '@playwright/test';

test('consultation des utilisateurs : inscription, connexion, liste, filtre, détail', async ({ page }) => {
  const email = `e2e-utilisateurs-${Date.now()}@example.com`;
  const password = 'MotDePasse123!';

  // 1. Bootstrap : créer un compte via le flux /register existant (aucun utilisateur seed n'existe)
  await page.goto('/register');
  await page.fill('#nom', 'Test');
  await page.fill('#prenom', 'E2E');
  await page.fill('#email', email);
  await page.fill('#mot_de_passe', password);
  await page.selectOption('#type_utilisateur', 'etudiant');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(/\/login$/);

  // 2. Connexion avec ce compte
  await page.fill('#email', email);
  await page.fill('#mot_de_passe', password);
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('http://localhost:4200/');

  // 3. Navigation vers la liste des utilisateurs
  await page.getByRole('link', { name: 'Utilisateurs' }).click();
  await expect(page).toHaveURL(/\/utilisateurs$/);
  await expect(page.locator('tr', { hasText: email })).toBeVisible();

  // 4. Filtre par type_utilisateur (client-side)
  await page.selectOption('#type-filter', 'etudiant');
  await expect(page.locator('tr', { hasText: email })).toBeVisible();
  await page.selectOption('#type-filter', 'professeur');
  await expect(page.locator('tr', { hasText: email })).toHaveCount(0);
  await page.selectOption('#type-filter', '');

  // 5. Clic sur la ligne -> détail en lecture seule
  await page.locator('tr', { hasText: email }).click();
  await expect(page).toHaveURL(/\/utilisateurs\/[0-9a-f-]+$/);
  await expect(page.locator('dd', { hasText: email })).toBeVisible();
  await expect(page.locator('dd', { hasText: 'etudiant' })).toBeVisible();
});
