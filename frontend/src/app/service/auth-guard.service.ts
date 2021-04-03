import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs';
import { filter, map, take } from 'rxjs/operators';
import { AuthFacadeService } from './auth-facade.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuardService implements CanActivate {

  constructor(
    private authFacade: AuthFacadeService,
    private router: Router
  ) { }

  /**
   * Allow the page to be activated only for a logged in user.
   * 
   * @param route - The guarded route
   * @param state - Snapshot of the route state
   * @returns Observable of a value whether the page can be activated
   */
  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> {
    return this.authFacade.user$.pipe(
      filter((user) => user !== undefined),
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
