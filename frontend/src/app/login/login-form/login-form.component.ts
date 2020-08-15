import { Component } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { AuthService } from 'src/app/api/services';

@Component({
  selector: 'app-login-form',
  templateUrl: './login-form.component.html',
  styleUrls: ['./login-form.component.scss']
})
export class LoginFormComponent {
  loginForm = this.fb.group({
    email: [null, Validators.required]
  });

  constructor(private fb: FormBuilder, private authService: AuthService) {}

  onSubmit() {
    this.authService.postApiAuthLogin(this.loginForm.value['email']).subscribe();
  }
}
