import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { AuthFacadeService } from 'src/app/service/auth-facade.service';
import { SnackService } from 'src/app/service/snack.service';
import { RegisterFormComponent } from '../register-form/register-form.component';

@Component({
  selector: 'app-login-form',
  templateUrl: './login-form.component.html',
  styleUrls: ['./login-form.component.scss']
})
export class LoginFormComponent implements OnInit {
  loginForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private authFacade: AuthFacadeService,
    private dialog: MatDialog,
    private dialogRef: MatDialogRef<LoginFormComponent>,
    private snackService: SnackService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loginForm = this.fb.group({
      email: [null, Validators.required],
      pwd: [null, Validators.required]
    });
  }

  /**
   * Try to log the user in.
   */
  submit() {
    this.authFacade
      .login(this.loginForm.value['email'], this.loginForm.value['pwd'])
      .subscribe(
        (user) => {
          this.snackService.snack(`Logged in as ${user.email}`);
          this.dialogRef.close()
          this.router.navigateByUrl('/project');
        },
        () => {
          this.snackService.snack('Could not log in');
        }
      );
  }

  /**
   * Open the register dialog and close this dialog.
   */
  goToRegistration() {
    this.dialog.open(RegisterFormComponent);
    this.dialogRef.close();
  }
}
