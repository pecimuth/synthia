import { Component } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { AuthFacadeService } from 'src/app/service/auth-facade.service';
import { MatDialogRef, MatDialog } from '@angular/material/dialog';
import { RegisterFormComponent } from '../register-form/register-form.component';
import { MatSnackBar } from '@angular/material/snack-bar';

const snackConfig = {
  duration: 2000
};

@Component({
  selector: 'app-login-form',
  templateUrl: './login-form.component.html',
  styleUrls: ['./login-form.component.scss']
})
export class LoginFormComponent {
  loginForm = this.fb.group({
    email: [null, Validators.required]
  });

  constructor(
    private fb: FormBuilder,
    private authFacade: AuthFacadeService,
    private dialog: MatDialog,
    private dialogRef: MatDialogRef<LoginFormComponent>,
    private snackBar: MatSnackBar
  ) {}

  onSubmit() {
    this.authFacade
      .login(this.loginForm.value['email'])
      .subscribe(
        (user) => {
          this.snackBar.open(`Logged in as ${user.email}`, 'OK', snackConfig);
          this.dialogRef.close()
        },
        () => {
          this.snackBar.open('Could not log in', 'OK', snackConfig);
        }
      );
  }

  goToRegistration() {
    this.dialog.open(RegisterFormComponent);
    this.dialogRef.close();
  }
}
