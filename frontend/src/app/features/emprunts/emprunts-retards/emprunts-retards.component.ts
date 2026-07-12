import { DatePipe } from '@angular/common';
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
  selector: 'app-emprunts-retards',
  standalone: true,
  imports: [DatePipe, RouterLink],
  templateUrl: './emprunts-retards.component.html',
  styleUrl: './emprunts-retards.component.css'
})
export class EmpruntsRetardsComponent implements OnInit {
  private readonly empruntsService = inject(EmpruntsService);
  private readonly livresService = inject(LivresService);
  private readonly utilisateursService = inject(UtilisateursService);

  private livresMap = new Map<string, Livre>();
  private utilisateursMap = new Map<string, Utilisateur>();

  emprunts: Emprunt[] = [];
  loading = false;
  errorMessage: string | null = null;

  ngOnInit(): void {
    this.loading = true;
    forkJoin({
      emprunts: this.empruntsService.getRetards(),
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
        this.errorMessage = 'Impossible de charger les emprunts en retard.';
        this.loading = false;
      }
    });
  }

  livreTitre(livreId: string): string {
    return this.livresMap.get(livreId)?.titre ?? livreId;
  }

  utilisateurNom(utilisateurId: string): string {
    const utilisateur = this.utilisateursMap.get(utilisateurId);
    return utilisateur ? `${utilisateur.prenom} ${utilisateur.nom}` : utilisateurId;
  }
}
