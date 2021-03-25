import { Component, OnInit, OnDestroy } from '@angular/core';
import { AuthFacadeService } from 'src/app/service/auth-facade.service';
import { UserView } from 'src/app/api/models/user-view';
import { Subject } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { LoginFormComponent } from 'src/app/dialog/login-form/login-form.component';
import { RegisterFormComponent } from 'src/app/dialog/register-form/register-form.component';
import { Router } from '@angular/router';
import { SnackService } from 'src/app/service/snack.service';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-user-menu',
  templateUrl: './user-menu.component.html',
  styleUrls: ['./user-menu.component.scss']
})
export class UserMenuComponent implements OnInit, OnDestroy {

  user: UserView;
  private unsubscribe$ = new Subject();

  constructor(
    private authFacade: AuthFacadeService,
    private dialog: MatDialog,
    private snackService: SnackService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.authFacade.user$
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(
        (user) => this.user = user
      );
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  openLoginDialog() {
    this.dialog.open(LoginFormComponent);
  }

  openRegisterDialog() {
    this.dialog.open(RegisterFormComponent);
  }

  logout() {
    this.authFacade.logout();
    this.router.navigateByUrl('/');
    this.snackService.snack('Logged out');
  }
}
