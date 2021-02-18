import { Component } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { AuthFacadeService } from 'src/app/service/auth-facade.service';
import { MatDialogRef, MatDialog } from '@angular/material/dialog';
import { RegisterFormComponent } from '../register-form/register-form.component';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Snack } from 'src/app/service/constants';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login-form',
  templateUrl: './login-form.component.html',
  styleUrls: ['./login-form.component.scss']
})
export class LoginFormComponent {
  loginForm = this.fb.group({
    email: [null, Validators.required],
    pwd: [null, Validators.required]
  });

  constructor(
    private fb: FormBuilder,
    private authFacade: AuthFacadeService,
    private dialog: MatDialog,
    private dialogRef: MatDialogRef<LoginFormComponent>,
    private snackBar: MatSnackBar,
    private router: Router
  ) {}

  onSubmit() {
    this.authFacade
      .login(this.loginForm.value['email'], this.loginForm.value['pwd'])
      .subscribe(
        (user) => {
          this.snackBar.open(`Logged in as ${user.email}`, Snack.OK, Snack.CONFIG);
          this.dialogRef.close()
          this.router.navigateByUrl('/project');
        },
        () => {
          this.snackBar.open('Could not log in', Snack.OK, Snack.CONFIG);
        }
      );
  }

  goToRegistration() {
    this.dialog.open(RegisterFormComponent);
    this.dialogRef.close();
  }
}
