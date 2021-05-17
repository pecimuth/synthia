import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { FormBuilder } from '@angular/forms';
import { MatButtonHarness } from '@angular/material/button/testing';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { SnackService } from 'src/app/service/snack.service';
import { Spy } from 'src/app/test';
import { ProjectFormComponent } from './project-form.component';


describe('ProjectFormComponent', () => {
  let component: ProjectFormComponent;
  let fixture: ComponentFixture<ProjectFormComponent>;
  let loader: HarnessLoader;

  const projectFacadeSpy = jasmine.createSpyObj(
    'ProjectFacadeService',
    ['createProject', 'renameProject']
  );

  const formBuilderSpy = Spy.formBuilder();
  const dialogRefSpy = Spy.dialogRef();
  const routerSpy = Spy.router();
  const snackServiceSpy = Spy.snackService();

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ ProjectFormComponent ],
      providers: [
        {provide: ProjectFacadeService, useValue: projectFacadeSpy},
        {provide: FormBuilder, useValue: formBuilderSpy},
        {provide: MatDialogRef, useValue: dialogRefSpy},
        {provide: Router, useValue: routerSpy},
        {provide: SnackService, useValue: snackServiceSpy},
        {provide: MAT_DIALOG_DATA, useValue: null}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProjectFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    loader = TestbedHarnessEnvironment.loader(fixture);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should not accept an empty form', async () => {
    const button = await loader.getHarness(MatButtonHarness.with({selector: '[type=submit]'}));
    await button.click();
    expect(projectFacadeSpy.createProject).not.toHaveBeenCalled();
    expect(projectFacadeSpy.renameProject).not.toHaveBeenCalled();
  });
});
