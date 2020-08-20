import { Injectable, OnDestroy } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { UserView } from '../api/models/user-view';
import { AuthService } from '../api/services';
import { tap } from 'rxjs/operators';
import { MessageView } from '../api/models/message-view';

@Injectable({
  providedIn: 'root'
})
export class AuthFacadeService implements OnDestroy {
  private _user$ = new BehaviorSubject<UserView>(null);
  get user$() {
    return this._user$;
  }

  constructor(
    private authService: AuthService
  ) { }

  ngOnDestroy() {
    this.user$.complete();
  }

  login(email: string): Observable<UserView> {
    return this.authService.postApiAuthLogin(email)
      .pipe(
        tap((user) => this._user$.next(user))
      );
  }

  register(email: string): Observable<UserView> {
    return this.authService.postApiAuthRegister(email)
      .pipe(
        tap((user) => this._user$.next(user))
      );
  }

  logout(): Observable<MessageView> {
    return this.authService.postApiAuthLogout()
      .pipe(
        tap(() => this._user$.next(null))
      );
  }

  refresh() {
    this.authService.getApiAuthUser()
      .subscribe(
        (user) => this._user$.next(user),
        () => this._user$.next(null)
      );
  }
}
