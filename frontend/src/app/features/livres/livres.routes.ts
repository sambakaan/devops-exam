import { Routes } from '@angular/router';

import { LivreFormComponent } from './livre-form/livre-form.component';
import { LivresListComponent } from './livres-list/livres-list.component';

export const livresRoutes: Routes = [
  { path: '', component: LivresListComponent },
  { path: 'nouveau', component: LivreFormComponent },
  { path: ':id/modifier', component: LivreFormComponent }
];
