import { Routes } from '@angular/router';

import { UtilisateurDetailComponent } from './utilisateur-detail/utilisateur-detail.component';
import { UtilisateursListComponent } from './utilisateurs-list/utilisateurs-list.component';

export const utilisateursRoutes: Routes = [
  { path: '', component: UtilisateursListComponent },
  { path: ':id', component: UtilisateurDetailComponent }
];
