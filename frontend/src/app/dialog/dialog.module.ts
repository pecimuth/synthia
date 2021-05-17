import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDialogModule } from '@angular/material/dialog';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { DatabaseSourceFormComponent } from './database-source-form/database-source-form.component';
import { FileSourceFormComponent } from './file-source-form/file-source-form.component';
import { FormFieldComponent } from './form-field/form-field.component';
import { LoginFormComponent } from './login-form/login-form.component';
import { ProjectFormComponent } from './project-form/project-form.component';
import { RegisterFormComponent } from './register-form/register-form.component';


@NgModule({
  declarations: [
    LoginFormComponent,
    RegisterFormComponent,
    ProjectFormComponent,
    DatabaseSourceFormComponent,
    FileSourceFormComponent,
    FormFieldComponent
  ],
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
    ProjectFormComponent,
    DatabaseSourceFormComponent,
    FileSourceFormComponent
  ],
  exports: [
    FormFieldComponent
  ]
})
export class DialogModule { }
