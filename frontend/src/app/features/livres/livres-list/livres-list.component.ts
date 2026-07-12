import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { debounceTime, distinctUntilChanged } from 'rxjs';

import { Livre } from '../livres.model';
import { LivresService } from '../livres.service';

@Component({
  selector: 'app-livres-list',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './livres-list.component.html',
  styleUrl: './livres-list.component.css'
})
export class LivresListComponent implements OnInit {
  private readonly livresService = inject(LivresService);

  readonly searchControl = new FormControl('', { nonNullable: true });

  livres: Livre[] = [];
  loading = false;
  errorMessage: string | null = null;
  successMessage: string | null = null;

  ngOnInit(): void {
    this.loadAll();

    this.searchControl.valueChanges.pipe(debounceTime(400), distinctUntilChanged()).subscribe((q) => {
      this.runSearch(q.trim());
    });
  }

  deleteLivre(livre: Livre): void {
    if (!confirm(`Supprimer "${livre.titre}" ?`)) {
      return;
    }

    this.errorMessage = null;
    this.livresService.delete(livre.id).subscribe({
      next: () => {
        this.livres = this.livres.filter((l) => l.id !== livre.id);
        this.successMessage = `"${livre.titre}" a été supprimé.`;
      },
      error: () => (this.errorMessage = 'Impossible de supprimer ce livre.')
    });
  }

  private loadAll(): void {
    this.loading = true;
    this.livresService.getAll().subscribe({
      next: (livres) => {
        this.livres = livres;
        this.loading = false;
      },
      error: () => {
        this.errorMessage = 'Impossible de charger les livres.';
        this.loading = false;
      }
    });
  }

  private runSearch(q: string): void {
    this.loading = true;
    this.errorMessage = null;
    const request$ = q ? this.livresService.search(q) : this.livresService.getAll();

    request$.subscribe({
      next: (livres) => {
        this.livres = livres;
        this.loading = false;
      },
      error: (err: HttpErrorResponse) => {
        this.errorMessage = err.error?.detail ?? 'Erreur lors de la recherche.';
        this.loading = false;
      }
    });
  }
}
