import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { Utilisateur } from '../utilisateurs.model';
import { UtilisateursService } from '../utilisateurs.service';

@Component({
  selector: 'app-utilisateur-detail',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './utilisateur-detail.component.html',
  styleUrl: './utilisateur-detail.component.css'
})
export class UtilisateurDetailComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly utilisateursService = inject(UtilisateursService);

  utilisateur: Utilisateur | null = null;
  loading = false;
  errorMessage: string | null = null;

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (!id) {
      this.errorMessage = 'Identifiant manquant.';
      return;
    }

    this.loading = true;
    this.utilisateursService.getOne(id).subscribe({
      next: (utilisateur) => {
        this.utilisateur = utilisateur;
        this.loading = false;
      },
      error: () => {
        this.errorMessage = 'Impossible de charger cet utilisateur.';
        this.loading = false;
      }
    });
  }
}
