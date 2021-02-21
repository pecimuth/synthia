import { Injectable, OnDestroy } from '@angular/core';
import { Observable, ReplaySubject } from 'rxjs';
import { UserView } from '../api/models/user-view';
import { AuthService } from '../api/services';
import { map, tap } from 'rxjs/operators';
import { UserAndTokenView } from '../api/models/user-and-token-view';
import { Constants } from './constants';

@Injectable({
  providedIn: 'root'
})
export class AuthFacadeService implements OnDestroy {
  private _user$ = new ReplaySubject<UserView>(1);
  private _isLoggedIn = false;

  get user$() {
    return this._user$;
  }

  get isLoggedIn(): boolean {
    return this._isLoggedIn;
  }

  constructor(
    private authService: AuthService
  ) { }

  ngOnDestroy() {
    this.user$.complete();
  }

  private nextUser(user: UserView) {
    this._isLoggedIn = !!user;
    this._user$.next(user);
  }

  private nextUserAndToken(userAndToken: UserAndTokenView) {
    localStorage.setItem(Constants.TOKEN_KEY, userAndToken.token);
    this.nextUser(userAndToken.user);
  }

  login(email: string, password: string): Observable<UserView> {
    return this.authService.postApiAuthLogin({
      email: email,
      pwd: password
    }).pipe(
        tap((userAndToken) => this.nextUserAndToken(userAndToken)),
        map((userAndToken) => userAndToken.user)
      );
  }

  register(email: string, password: string): Observable<UserView> {
    return this.authService.postApiAuthRegister({
      email: email,
      pwd: password
    }).pipe(
        tap((userAndToken) => this.nextUserAndToken(userAndToken)),
        map((userAndToken) => userAndToken.user)
      );
  }

  logout() {
    localStorage.removeItem(Constants.TOKEN_KEY);
    this.nextUser(null);
  }

  refresh() {
    this.authService.getApiAuthUser()
      .subscribe(
        (user) => this.nextUser(user),
        () => this.nextUser(null)
      );
  }
}
