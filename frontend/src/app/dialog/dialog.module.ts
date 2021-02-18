import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginFormComponent } from './login-form/login-form.component';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { ReactiveFormsModule } from '@angular/forms';
import { MatDialogModule } from '@angular/material/dialog';
import { RegisterFormComponent } from './register-form/register-form.component';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { CreateProjectFormComponent } from './create-project-form/create-project-form.component';
import { MatSelectModule } from '@angular/material/select';
import { DatabaseSourceFormComponent } from './database-source-form/database-source-form.component';
import { FileSourceFormComponent } from './file-source-form/file-source-form.component';
import { FormFieldComponent } from './form-field/form-field.component';


@NgModule({
  declarations: [LoginFormComponent, RegisterFormComponent, CreateProjectFormComponent, DatabaseSourceFormComponent, FileSourceFormComponent, FormFieldComponent],
  imports: [
    CommonModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatSnackBarModule,
    MatSelectModule
  ],
  entryComponents: [
    LoginFormComponent,
    RegisterFormComponent,
    CreateProjectFormComponent,
    DatabaseSourceFormComponent,
    FileSourceFormComponent
  ]
})
export class DialogModule { }
