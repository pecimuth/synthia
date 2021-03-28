import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';

import { LoginFormComponent } from './login-form.component';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { Spy } from 'src/app/test';
import { SnackService } from 'src/app/service/snack.service';
import { Router } from '@angular/router';
import { AuthFacadeService } from 'src/app/service/auth-facade.service';

describe('LoginFormComponent', () => {
  let component: LoginFormComponent;
  let fixture: ComponentFixture<LoginFormComponent>;

  const authFacadeSpy = jasmine.createSpyObj(
    'AuthFacadeService',
    ['login']
  );

  const formBuilderSpy = Spy.formBuilder();
  formBuilderSpy.group.and.returnValue({controls: {}});

  const dialogRefSpy = Spy.dialogRef();
  const snackServiceSpy = Spy.snackService();
  const routerSpy = Spy.router();
  const matDialogSpy = Spy.matDialog();

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ LoginFormComponent ],
      imports: [
        MatButtonModule,
        MatInputModule
      ],
      providers: [
        {provide: FormBuilder, useValue: formBuilderSpy},
        {provide: MatDialogRef, useValue: dialogRefSpy},
        {provide: SnackService, useValue: snackServiceSpy},
        {provide: Router, useValue: routerSpy},
        {provide: MatDialog, useValue: matDialogSpy},
        {provide: AuthFacadeService, useValue: authFacadeSpy}
      ]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LoginFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should compile', () => {
    expect(component).toBeTruthy();
  });
});
