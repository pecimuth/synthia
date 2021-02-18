import { Component, OnInit, OnDestroy } from '@angular/core';
import { AuthFacadeService } from 'src/app/service/auth-facade.service';
import { UserView } from 'src/app/api/models/user-view';
import { Subscription } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { LoginFormComponent } from 'src/app/dialog/login-form/login-form.component';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Snack } from 'src/app/service/constants';
import { RegisterFormComponent } from 'src/app/dialog/register-form/register-form.component';
import { Router } from '@angular/router';

@Component({
  selector: 'app-user-menu',
  templateUrl: './user-menu.component.html',
  styleUrls: ['./user-menu.component.scss']
})
export class UserMenuComponent implements OnInit, OnDestroy {

  user: UserView;
  private userSub: Subscription;

  constructor(
    private authFacade: AuthFacadeService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.userSub = this.authFacade.user$
      .subscribe(
        (user) => this.user = user
      );
  }

  ngOnDestroy() {
    this.userSub.unsubscribe();
  }

  openLoginDialog() {
    this.dialog.open(LoginFormComponent);
  }

  openRegisterDialog() {
    this.dialog.open(RegisterFormComponent);
  }

  onLogout() {
    this.authFacade.logout()
      .subscribe(
        () => {
          this.router.navigateByUrl('/');
          this.snackBar.open('Logged out', Snack.OK, Snack.CONFIG);}
        );
    ;
  }
}
