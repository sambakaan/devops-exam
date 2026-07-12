import { DatePipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';

import { Livre } from '../../livres/livres.model';
import { LivresService } from '../../livres/livres.service';
import { Utilisateur } from '../../utilisateurs/utilisateurs.model';
import { UtilisateursService } from '../../utilisateurs/utilisateurs.service';
import { Emprunt } from '../emprunts.model';
import { EmpruntsService } from '../emprunts.service';

@Component({
  selector: 'app-emprunts-list',
  standalone: true,
  imports: [DatePipe, RouterLink],
  templateUrl: './emprunts-list.component.html',
  styleUrl: './emprunts-list.component.css'
})
export class EmpruntsListComponent implements OnInit {
  private readonly empruntsService = inject(EmpruntsService);
  private readonly livresService = inject(LivresService);
  private readonly utilisateursService = inject(UtilisateursService);

  private livresMap = new Map<string, Livre>();
  private utilisateursMap = new Map<string, Utilisateur>();

  emprunts: Emprunt[] = [];
  loading = false;
  errorMessage: string | null = null;

  ngOnInit(): void {
    this.loadAll();
  }

  livreTitre(livreId: string): string {
    return this.livresMap.get(livreId)?.titre ?? livreId;
  }

  utilisateurNom(utilisateurId: string): string {
    const utilisateur = this.utilisateursMap.get(utilisateurId);
    return utilisateur ? `${utilisateur.prenom} ${utilisateur.nom}` : utilisateurId;
  }

  retourner(emprunt: Emprunt): void {
    this.errorMessage = null;
    this.empruntsService.retour(emprunt.id).subscribe({
      next: () => this.loadAll(),
      error: (err: HttpErrorResponse) => {
        this.errorMessage = err.error?.detail ?? 'Une erreur est survenue.';
      }
    });
  }

  private loadAll(): void {
    this.loading = true;
    forkJoin({
      emprunts: this.empruntsService.getAll(),
      livres: this.livresService.getAll(),
      utilisateurs: this.utilisateursService.getAll()
    }).subscribe({
      next: ({ emprunts, livres, utilisateurs }) => {
        this.livresMap = new Map(livres.map((livre) => [livre.id, livre]));
        this.utilisateursMap = new Map(utilisateurs.map((utilisateur) => [utilisateur.id, utilisateur]));
        this.emprunts = emprunts;
        this.loading = false;
      },
      error: () => {
        this.errorMessage = 'Impossible de charger les emprunts.';
        this.loading = false;
      }
    });
  }
}
