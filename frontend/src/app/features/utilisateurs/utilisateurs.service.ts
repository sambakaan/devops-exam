import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { Utilisateur } from './utilisateurs.model';

@Injectable({ providedIn: 'root' })
export class UtilisateursService {
  private readonly baseUrl = `${environment.utilisateursServiceUrl}/users`;

  constructor(private readonly http: HttpClient) {}

  getAll(): Observable<Utilisateur[]> {
    return this.http.get<Utilisateur[]>(this.baseUrl);
  }

  getOne(id: string): Observable<Utilisateur> {
    return this.http.get<Utilisateur>(`${this.baseUrl}/${id}`);
  }
}
