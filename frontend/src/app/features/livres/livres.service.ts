import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { Livre, LivreCreate, LivreUpdate } from './livres.model';

@Injectable({ providedIn: 'root' })
export class LivresService {
  private readonly baseUrl = `${environment.livresServiceUrl}/livres`;

  constructor(private readonly http: HttpClient) {}

  getAll(): Observable<Livre[]> {
    return this.http.get<Livre[]>(this.baseUrl);
  }

  getOne(id: string): Observable<Livre> {
    return this.http.get<Livre>(`${this.baseUrl}/${id}`);
  }

  search(q: string): Observable<Livre[]> {
    return this.http.get<Livre[]>(`${this.baseUrl}/search`, { params: { q } });
  }

  create(payload: LivreCreate): Observable<Livre> {
    return this.http.post<Livre>(this.baseUrl, payload);
  }

  update(id: string, payload: LivreUpdate): Observable<Livre> {
    return this.http.put<Livre>(`${this.baseUrl}/${id}`, payload);
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/${id}`);
  }
}
