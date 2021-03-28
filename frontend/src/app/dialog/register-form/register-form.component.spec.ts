import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { FormBuilder } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { AuthFacadeService } from 'src/app/service/auth-facade.service';
import { SnackService } from 'src/app/service/snack.service';
import { Spy } from 'src/app/test';

import { RegisterFormComponent } from './register-form.component';

describe('RegisterFormComponent', () => {
  let component: RegisterFormComponent;
  let fixture: ComponentFixture<RegisterFormComponent>;

  const authFacadeSpy = jasmine.createSpyObj(
    'AuthFacadeService',
    ['register']
  );

  const formBuilderSpy = Spy.formBuilder();
  formBuilderSpy.group.and.returnValue({controls: {}});

  const dialogRefSpy = Spy.dialogRef();
  const snackServiceSpy = Spy.snackService();

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ RegisterFormComponent ],
      providers: [
        {provide: FormBuilder, useValue: formBuilderSpy},
        {provide: MatDialogRef, useValue: dialogRefSpy},
        {provide: SnackService, useValue: snackServiceSpy},
        {provide: AuthFacadeService, useValue: authFacadeSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RegisterFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
