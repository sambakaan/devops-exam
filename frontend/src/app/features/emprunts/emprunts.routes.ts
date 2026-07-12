import { Routes } from '@angular/router';

import { EmpruntFormComponent } from './emprunt-form/emprunt-form.component';
import { EmpruntsListComponent } from './emprunts-list/emprunts-list.component';
import { EmpruntsRetardsComponent } from './emprunts-retards/emprunts-retards.component';

export const empruntsRoutes: Routes = [
  { path: '', component: EmpruntsListComponent },
  { path: 'nouveau', component: EmpruntFormComponent },
  { path: 'retards', component: EmpruntsRetardsComponent }
];
