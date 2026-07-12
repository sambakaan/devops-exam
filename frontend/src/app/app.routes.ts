import { Routes } from '@angular/router';

import { authGuard } from './core/guards/auth.guard';
import { LayoutComponent } from './core/layout/layout.component';
import { LoginComponent } from './features/auth/login/login.component';
import { RegisterComponent } from './features/auth/register/register.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  {
    path: '',
    component: LayoutComponent,
    canActivate: [authGuard],
    children: [
      {
        path: 'livres',
        canActivate: [authGuard],
        loadChildren: () => import('./features/livres/livres.routes').then((m) => m.livresRoutes)
      },
      {
        path: 'utilisateurs',
        canActivate: [authGuard],
        loadChildren: () => import('./features/utilisateurs/utilisateurs.routes').then((m) => m.utilisateursRoutes)
      },
      {
        path: 'emprunts',
        canActivate: [authGuard],
        loadChildren: () => import('./features/emprunts/emprunts.routes').then((m) => m.empruntsRoutes)
      }
    ]
  },
  { path: '**', redirectTo: 'login' }
];
