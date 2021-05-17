import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { FormBuilder } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { MatInputModule } from '@angular/material/input';
import { Router } from '@angular/router';
import { AuthFacadeService } from 'src/app/service/auth-facade.service';
import { SnackService } from 'src/app/service/snack.service';
import { Spy } from 'src/app/test';
import { LoginFormComponent } from './login-form.component';


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
