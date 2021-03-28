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

  /**
   * Replay subject of the logged in user.
   */
  private _user$ = new ReplaySubject<UserView>(1);

  /**
   * Do we have a logged in user?
   */
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

  /**
   * Try to log in a user via the API.
   * 
   * @param email - The user's email
   * @param password - The entered password
   * @returns Observable of the logged in user
   */
  login(email: string, password: string): Observable<UserView> {
    return this.authService.postApiAuthLogin({
      email: email,
      pwd: password
    }).pipe(
        tap((userAndToken) => this.nextUserAndToken(userAndToken)),
        map((userAndToken) => userAndToken.user)
      );
  }

  /**
   * Register a new user.
   * 
   * @param email - The new user's email
   * @param password - The new user's password
   * @returns Observable of the registered user
   */
  register(email: string, password: string): Observable<UserView> {
    return this.authService.postApiAuthRegister({
      email: email,
      pwd: password
    }).pipe(
        tap((userAndToken) => this.nextUserAndToken(userAndToken)),
        map((userAndToken) => userAndToken.user)
      );
  }

  /**
   * Log out the user. The auth token is forgotten.
   */
  logout() {
    localStorage.removeItem(Constants.TOKEN_KEY);
    this.nextUser(null);
  }

  /**
   * Refresh the logged in user's information.
   */
  refresh() {
    this.authService.getApiAuthUser()
      .subscribe(
        (user) => this.nextUser(user),
        () => this.nextUser(null)
      );
  }
}
