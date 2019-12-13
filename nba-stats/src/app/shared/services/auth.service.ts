import { Observable, ReplaySubject, Observer, of } from 'rxjs';
import { Injectable } from '@angular/core';
import { Config } from 'protractor';
import { Router } from '@angular/router';
import { map, finalize } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { URLS } from 'src/environments/environment';
import { User } from '../interface/user.interface';

@Injectable()
export class AuthService {

  private _token: string = null;
  private _user: User = null;
  private _endpoints: Config;

  constructor(
    private _router: Router,
    private _httpClient: HttpClient,
  ) { }

  private _fetchApiToken(username: string, password: string) {
    return this._httpClient.post<{token: string}>(
      URLS.login,
      {username, password}
    ).pipe(
      map(
        (response: {token: string}) => {
          this._token = response.token;
          localStorage['token'] = response.token;
          return response;
        }
      )
    );
  }

  fetchUserData(): Observable<User> {
    return this._httpClient.get<User>(URLS.user);
  }

  authenticateUser(user: User) {
    this._user = user;
  }

  private _unauthenticateUser() {
    this._user = null;
    this._token = null;
    localStorage['token'] = null;
  }

  logout() {
    this._unauthenticateUser();
  }

  login(username: string, password: string): Observable<string> {
    return Observable.create(
      (observer: Observer<string>) => this._fetchApiToken(username, password).subscribe(
        () => {
          observer.next(null);
        },
        error => observer.error(this._getError(error))
      )
    ).pipe(
      map((response: {token: string}) => {
        this.fetchUserData().subscribe((user: User) => {
          this.authenticateUser(user);
        });
      })
    );
  }

  getToken(): string {
    return this._token;
  }

  getUserFullName(): string {
    return this._user.last_name && this._user.first_name ? `${this._user.first_name} ${this._user.last_name}` : this._user.username;
  }

  getUserUsername(): string {
    return this._user ? this._user.username : '';
  }

  getUserCredits(): number {
    return this._user ? this._user.credits : 0;
  }

  isAdmin(): boolean {
    return this._user ? this._user.is_superuser : false;
  }

  isAuthenticated(): boolean {
    return ![this._token].includes(null);
  }

  shouldBeAuthenticated(): Observable<boolean> {
    this._token = localStorage['token'];
    return !this._token ? of(false) : this.fetchUserData().pipe(
      map(
        (response: User) => {
          this.authenticateUser(response);
          return true;
        }
      )
    );
  }

  _getError(err): string {
    return err.status === 400 ? err.error['non_field_errors'][0] : 'Error connecting server';
  }

}
