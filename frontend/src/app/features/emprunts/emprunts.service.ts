import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { Emprunt, EmpruntCreate } from './emprunts.model';

@Injectable({ providedIn: 'root' })
export class EmpruntsService {
  private readonly baseUrl = `${environment.empruntsServiceUrl}/emprunts`;

  constructor(private readonly http: HttpClient) {}

  getAll(): Observable<Emprunt[]> {
    return this.http.get<Emprunt[]>(this.baseUrl);
  }

  getByUtilisateur(utilisateurId: string): Observable<Emprunt[]> {
    return this.http.get<Emprunt[]>(`${this.baseUrl}/utilisateur/${utilisateurId}`);
  }

  getRetards(): Observable<Emprunt[]> {
    return this.http.get<Emprunt[]>(`${this.baseUrl}/retards`);
  }

  create(payload: EmpruntCreate): Observable<Emprunt> {
    return this.http.post<Emprunt>(this.baseUrl, payload);
  }

  retour(id: string): Observable<Emprunt> {
    return this.http.put<Emprunt>(`${this.baseUrl}/${id}/retour`, null);
  }
}
