import { Injectable, OnDestroy } from '@angular/core';
import { Observable, ReplaySubject } from 'rxjs';
import { UserView } from '../api/models/user-view';
import { AuthService } from '../api/services';
import { tap } from 'rxjs/operators';
import { MessageView } from '../api/models/message-view';

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

  login(email: string, password: string): Observable<UserView> {
    return this.authService.postApiAuthLogin({
      email: email,
      pwd: password
    }).pipe(
        tap((user) => this.nextUser(user))
      );
  }

  register(email: string, password: string): Observable<UserView> {
    return this.authService.postApiAuthRegister({
      email: email,
      pwd: password
    }).pipe(
        tap((user) => this.nextUser(user))
      );
  }

  logout(): Observable<MessageView> {
    return this.authService.postApiAuthLogout()
      .pipe(
        tap(() => this.nextUser(null))
      );
  }

  refresh() {
    this.authService.getApiAuthUser()
      .subscribe(
        (user) => this.nextUser(user),
        () => this.nextUser(null)
      );
  }
}
