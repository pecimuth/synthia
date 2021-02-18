import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';
import { map, take } from 'rxjs/operators';
import { AuthFacadeService } from './auth-facade.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuardService implements CanActivate {

  constructor(
    private authFacade: AuthFacadeService,
    private router: Router
  ) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> {
    return this.authFacade.user$.pipe(
      take(1),
      map((user) => {
        const loggedIn = !!user;
        if (!loggedIn) {
          this.router.navigateByUrl('/');
        }
        return loggedIn;
      })
    );
  }
}
