import { Component, OnInit, inject } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { TYPES_UTILISATEUR, Utilisateur } from '../utilisateurs.model';
import { UtilisateursService } from '../utilisateurs.service';

@Component({
  selector: 'app-utilisateurs-list',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './utilisateurs-list.component.html',
  styleUrl: './utilisateurs-list.component.css'
})
export class UtilisateursListComponent implements OnInit {
  private readonly utilisateursService = inject(UtilisateursService);
  private readonly router = inject(Router);

  readonly typesUtilisateur = TYPES_UTILISATEUR;
  readonly typeFilterControl = new FormControl<'' | Utilisateur['type_utilisateur']>('', { nonNullable: true });

  private allUtilisateurs: Utilisateur[] = [];
  utilisateurs: Utilisateur[] = [];
  loading = false;
  errorMessage: string | null = null;

  ngOnInit(): void {
    this.loading = true;
    this.utilisateursService.getAll().subscribe({
      next: (utilisateurs) => {
        this.allUtilisateurs = utilisateurs;
        this.utilisateurs = utilisateurs;
        this.loading = false;
      },
      error: () => {
        this.errorMessage = 'Impossible de charger les utilisateurs.';
        this.loading = false;
      }
    });

    this.typeFilterControl.valueChanges.subscribe((type) => {
      this.utilisateurs = type ? this.allUtilisateurs.filter((u) => u.type_utilisateur === type) : this.allUtilisateurs;
    });
  }

  viewDetail(id: string): void {
    this.router.navigate(['/utilisateurs', id]);
  }
}
