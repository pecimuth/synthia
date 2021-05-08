import { Component, OnInit } from '@angular/core';
import { Validators, FormBuilder } from '@angular/forms';
import { AuthFacadeService } from 'src/app/service/auth-facade.service';
import { MatDialogRef } from '@angular/material/dialog';
import { SnackService } from 'src/app/service/snack.service';

@Component({
  selector: 'app-register-form',
  templateUrl: './register-form.component.html',
  styleUrls: ['./register-form.component.scss']
})
export class RegisterFormComponent implements OnInit {
  registerForm = this.fb.group({
    email: [null, Validators.required],
    pwd: [null, Validators.required]
  });

  constructor(
    private fb: FormBuilder,
    private authFacade: AuthFacadeService,
    private dialogRef: MatDialogRef<RegisterFormComponent>,
    private snackService: SnackService
  ) {}

  ngOnInit() {}

  /**
   * Patch the logged in user or register a new user.
   * 
   * In case we have a logged in user, change their email and password.
   * Otherwise register a new user.
   */
  submit() {
    if (!this.registerForm.valid) {
      return;
    }

    const user = this.authFacade.user$.value;

    const action = (user)
      ? this.authFacade.patch(this.registerForm.value['email'], this.registerForm.value['pwd'])
      : this.authFacade.register(this.registerForm.value['email'], this.registerForm.value['pwd']);

      action.subscribe(
        (user) => {
          this.snackService.snack(`Logged in as ${user.email}`);
          this.dialogRef.close()
        },
        (err) => {
          this.snackService.errorIntoSnack(err, 'Could not register an account');
        }
      );
  }
}
