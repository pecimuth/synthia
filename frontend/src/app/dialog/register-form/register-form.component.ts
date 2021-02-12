import { Component, OnInit } from '@angular/core';
import { Validators, FormBuilder } from '@angular/forms';
import { AuthFacadeService } from 'src/app/service/auth-facade.service';
import { MatDialogRef } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Snack } from 'src/app/service/constants';

@Component({
  selector: 'app-register-form',
  templateUrl: './register-form.component.html',
  styleUrls: ['./register-form.component.scss']
})
export class RegisterFormComponent implements OnInit {
  registerForm = this.fb.group({
    email: [null, Validators.required]
  });

  constructor(
    private fb: FormBuilder,
    private authFacade: AuthFacadeService,
    private dialogRef: MatDialogRef<RegisterFormComponent>,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit() {}
  
  onSubmit() {
    this.authFacade
      .register(this.registerForm.value['email'])
      .subscribe(
        (user) => {
          this.snackBar.open(`Logged in as ${user.email}`, Snack.OK, Snack.CONFIG);
          this.dialogRef.close()
        },
        () => {
          this.snackBar.open('Could not register an account', Snack.OK, Snack.CONFIG);
        }
      );
  }
}
