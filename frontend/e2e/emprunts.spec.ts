import { test, expect } from '@playwright/test';

test("cycle de vie d'un emprunt : création, refus si indisponible, retour", async ({ page, context }) => {
  const timestamp = Date.now();
  const email = `e2e-emprunts-${timestamp}@example.com`;
  const password = 'MotDePasse123!';
  const titre = `Livre E2E ${timestamp}`;
  const isbn = `ISBN-${timestamp}`;

  // 1. Bootstrap : inscription + connexion sur la page A
  await page.goto('/register');
  await page.fill('#nom', 'Test');
  await page.fill('#prenom', 'Emprunts');
  await page.fill('#email', email);
  await page.fill('#mot_de_passe', password);
  await page.selectOption('#type_utilisateur', 'etudiant');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(/\/login$/);

  await page.fill('#email', email);
  await page.fill('#mot_de_passe', password);
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('http://localhost:4200/');

  // 2. Créer un livre à exemplaire unique (quantite_totale = 1)
  await page.goto('/livres/nouveau');
  await page.fill('#titre', titre);
  await page.fill('#auteur', 'Auteur E2E');
  await page.fill('#isbn', isbn);
  await page.fill('#quantite_totale', '1');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(/\/livres$/);
  await expect(page.locator('tr', { hasText: titre })).toContainText('1 / 1');

  // 3. Premier emprunt réussi (page A reste ensuite sur /emprunts/nouveau, liste non rafraîchie)
  await page.goto('/emprunts/nouveau');

  const livreOptionValue = await page.locator('#livre-select option', { hasText: titre }).getAttribute('value');
  const utilisateurOptionValue = await page
    .locator('#utilisateur-select option', { hasText: email })
    .getAttribute('value');
  expect(livreOptionValue).toBeTruthy();
  expect(utilisateurOptionValue).toBeTruthy();

  await page.selectOption('#livre-select', livreOptionValue!);
  await page.selectOption('#utilisateur-select', utilisateurOptionValue!);
  await page.click('button[type="submit"]');
  await expect(page.locator('.form-success')).toHaveText('Emprunt créé avec succès.');

  // 4. Page B (même contexte, même localStorage) constate la disponibilité décrémentée
  const pageB = await context.newPage();
  await pageB.goto('/livres');
  await expect(pageB.locator('tr', { hasText: titre })).toContainText('0 / 1');

  // 5. Page A retente le même emprunt sur son formulaire non rafraîchi (le backend doit refuser)
  await page.selectOption('#livre-select', livreOptionValue!);
  await page.selectOption('#utilisateur-select', utilisateurOptionValue!);
  await page.click('button[type="submit"]');
  await expect(page.locator('.form-error')).toContainText("n'a plus d'exemplaire disponible");

  // 6. Page B retourne l'emprunt depuis /emprunts, la liste se met à jour sans navigation
  await pageB.goto('/emprunts');
  const row = pageB.locator('tr', { hasText: titre });
  await expect(row).toBeVisible();
  await row.getByRole('button', { name: 'Retourner' }).click();
  await expect(row.locator('.badge')).toHaveText('retourne');

  // 7. Page B constate que la disponibilité est revenue à 1/1
  await pageB.goto('/livres');
  await expect(pageB.locator('tr', { hasText: titre })).toContainText('1 / 1');
});
