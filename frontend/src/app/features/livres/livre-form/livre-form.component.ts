import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { LivresService } from '../livres.service';

@Component({
  selector: 'app-livre-form',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './livre-form.component.html',
  styleUrl: './livre-form.component.css'
})
export class LivreFormComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly livresService = inject(LivresService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  livreId: string | null = null;
  errorMessage: string | null = null;

  readonly form = this.fb.nonNullable.group({
    titre: ['', [Validators.required]],
    auteur: ['', [Validators.required]],
    isbn: ['', [Validators.required]],
    quantite_totale: [1, [Validators.required, Validators.min(1)]]
  });

  get isEditMode(): boolean {
    return this.livreId !== null;
  }

  ngOnInit(): void {
    this.livreId = this.route.snapshot.paramMap.get('id');
    if (!this.livreId) {
      return;
    }

    this.livresService.getOne(this.livreId).subscribe({
      next: (livre) =>
        this.form.patchValue({
          titre: livre.titre,
          auteur: livre.auteur,
          isbn: livre.isbn,
          quantite_totale: livre.quantite_totale
        }),
      error: () => (this.errorMessage = 'Livre introuvable.')
    });
  }

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.errorMessage = null;
    const payload = this.form.getRawValue();
    const request$ = this.isEditMode
      ? this.livresService.update(this.livreId!, payload)
      : this.livresService.create(payload);

    request$.subscribe({
      next: () => this.router.navigate(['/livres']),
      error: (err: HttpErrorResponse) => {
        this.errorMessage = err.error?.detail ?? 'Une erreur est survenue.';
      }
    });
  }
}
