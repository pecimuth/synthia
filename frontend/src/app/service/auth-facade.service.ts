import { Injectable, OnDestroy } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { UserAndTokenView } from '../api/models/user-and-token-view';
import { UserView } from '../api/models/user-view';
import { AuthService } from '../api/services';
import { Constants } from './constants';

@Injectable({
  providedIn: 'root'
})
export class AuthFacadeService implements OnDestroy {

  /**
   * Behavior subject of the logged in user.
   * Value of undefined means that we have not fetched the user yet.
   * Value of null means that there is no logged in user.
   */
  user$ = new BehaviorSubject<UserView>(undefined);

  /**
   * Do we have a logged in user?
   */
  get isLoggedIn(): boolean {
    return !!this.user$.value;
  }

  constructor(
    private authService: AuthService
  ) { }

  ngOnDestroy() {
    this.user$.complete();
  }

  private nextUserAndToken(userAndToken: UserAndTokenView) {
    localStorage.setItem(Constants.TOKEN_KEY, userAndToken.token);
    this.user$.next(userAndToken.user);
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
    this.user$.next(null);
  }

  /**
   * Refresh the logged in user's information.
   */
  refresh() {
    this.authService.getApiAuthUser()
      .subscribe(
        (user) => this.user$.next(user),
        () => this.user$.next(null)
      );
  }
}
