import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { UserView } from '../api/models/user-view';
import { AuthService } from '../api/services';

@Injectable({
  providedIn: 'root'
})
export class AuthFacadeService {
  private _user$ = new BehaviorSubject<UserView>(null);
  get user$() {
    return this._user$;
  }

  constructor(
    private authService: AuthService
  ) { }

  complete() {
    this.user$.complete();
  }

  login(email: string) {
    this.authService.postApiAuthLogin(email)
      .subscribe(
        (user) => this._user$.next(user)
      );
  }

  logout() {
    this.authService.postApiAuthLogout()
      .subscribe(
        () => this._user$.next(null)
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
