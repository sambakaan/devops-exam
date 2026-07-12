import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { AuthService } from '../../../core/services/auth.service';
import { TypeUtilisateur } from '../../../core/models/user.model';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  private readonly fb = inject(FormBuilder);
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  readonly typesUtilisateur: TypeUtilisateur[] = ['etudiant', 'professeur', 'personnel_administratif'];

  readonly form = this.fb.nonNullable.group({
    nom: ['', [Validators.required]],
    prenom: ['', [Validators.required]],
    email: ['', [Validators.required, Validators.email]],
    mot_de_passe: ['', [Validators.required]],
    type_utilisateur: this.fb.nonNullable.control<TypeUtilisateur>('etudiant', [Validators.required])
  });

  errorMessage: string | null = null;

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.errorMessage = null;
    this.authService.register(this.form.getRawValue()).subscribe({
      next: () => this.router.navigate(['/login']),
      error: () => (this.errorMessage = 'Impossible de créer le compte (email déjà utilisé ?).')
    });
  }
}
