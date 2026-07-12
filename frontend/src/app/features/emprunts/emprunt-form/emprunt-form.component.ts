import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';

import { Livre } from '../../livres/livres.model';
import { LivresService } from '../../livres/livres.service';
import { Utilisateur } from '../../utilisateurs/utilisateurs.model';
import { UtilisateursService } from '../../utilisateurs/utilisateurs.service';
import { EmpruntsService } from '../emprunts.service';

@Component({
  selector: 'app-emprunt-form',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './emprunt-form.component.html',
  styleUrl: './emprunt-form.component.css'
})
export class EmpruntFormComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly empruntsService = inject(EmpruntsService);
  private readonly livresService = inject(LivresService);
  private readonly utilisateursService = inject(UtilisateursService);

  livresDisponibles: Livre[] = [];
  utilisateurs: Utilisateur[] = [];
  loading = false;
  errorMessage: string | null = null;
  successMessage: string | null = null;

  readonly form = this.fb.nonNullable.group({
    livre_id: ['', [Validators.required]],
    utilisateur_id: ['', [Validators.required]]
  });

  ngOnInit(): void {
    this.loading = true;
    forkJoin({
      livres: this.livresService.getAll(),
      utilisateurs: this.utilisateursService.getAll()
    }).subscribe({
      next: ({ livres, utilisateurs }) => {
        this.livresDisponibles = livres.filter((livre) => livre.quantite_disponible > 0);
        this.utilisateurs = utilisateurs;
        this.loading = false;
      },
      error: () => {
        this.errorMessage = 'Impossible de charger les livres et utilisateurs.';
        this.loading = false;
      }
    });
  }

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.errorMessage = null;
    this.successMessage = null;
    const payload = this.form.getRawValue();

    this.empruntsService.create(payload).subscribe({
      next: () => {
        this.successMessage = 'Emprunt créé avec succès.';
        this.form.reset({ livre_id: '', utilisateur_id: '' });
      },
      error: (err: HttpErrorResponse) => {
        this.errorMessage = err.error?.detail ?? 'Une erreur est survenue.';
      }
    });
  }
}
