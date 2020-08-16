import { Component } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { AuthFacadeService } from 'src/app/service/auth-facade.service';

@Component({
  selector: 'app-login-form',
  templateUrl: './login-form.component.html',
  styleUrls: ['./login-form.component.scss']
})
export class LoginFormComponent {
  loginForm = this.fb.group({
    email: [null, Validators.required]
  });

  constructor(private fb: FormBuilder, private authFacade: AuthFacadeService) {}

  onSubmit() {
    this.authFacade.login(this.loginForm.value['email']);
  }
}
