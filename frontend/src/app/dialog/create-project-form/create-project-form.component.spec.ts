import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormBuilder } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { SnackService } from 'src/app/service/snack.service';
import { Spy } from 'src/app/test';

import { CreateProjectFormComponent } from './create-project-form.component';

describe('CreateProjectFormComponent', () => {
  let component: CreateProjectFormComponent;
  let fixture: ComponentFixture<CreateProjectFormComponent>;

  const projectFacadeSpy = jasmine.createSpyObj(
    'ProjectFacadeService',
    ['createProject']
  );

  const formBuilderSpy = Spy.formBuilder();
  const dialogRefSpy = Spy.dialogRef();
  const routerSpy = Spy.router();
  const snackServiceSpy = Spy.snackService();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CreateProjectFormComponent ],
      providers: [
        {provide: ProjectFacadeService, useValue: projectFacadeSpy},
        {provide: FormBuilder, useValue: formBuilderSpy},
        {provide: MatDialogRef, useValue: dialogRefSpy},
        {provide: Router, useValue: routerSpy},
        {provide: SnackService, useValue: snackServiceSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateProjectFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
