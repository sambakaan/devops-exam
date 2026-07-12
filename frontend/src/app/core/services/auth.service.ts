import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, map, tap } from 'rxjs';

import { environment } from '../../../environments/environment';
import { AuthResponse, LoginPayload, RegisterPayload, User } from '../models/user.model';

const TOKEN_KEY = 'auth_token';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly tokenSubject = new BehaviorSubject<string | null>(localStorage.getItem(TOKEN_KEY));
  readonly isAuthenticated$ = this.tokenSubject.pipe(map((token) => !!token));

  constructor(private readonly http: HttpClient) {}

  register(payload: RegisterPayload): Observable<User> {
    return this.http.post<User>(`${environment.utilisateursServiceUrl}/auth/register`, payload);
  }

  login(payload: LoginPayload): Observable<AuthResponse> {
    return this.http
      .post<AuthResponse>(`${environment.utilisateursServiceUrl}/auth/login`, payload)
      .pipe(tap((response) => this.setToken(response.access_token)));
  }

  logout(): void {
    localStorage.removeItem(TOKEN_KEY);
    this.tokenSubject.next(null);
  }

  getToken(): string | null {
    return this.tokenSubject.value;
  }

  isAuthenticated(): boolean {
    return !!this.tokenSubject.value;
  }

  private setToken(token: string): void {
    localStorage.setItem(TOKEN_KEY, token);
    this.tokenSubject.next(token);
  }
}
