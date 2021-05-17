import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { FormBuilder, FormsModule } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { SnackService } from 'src/app/service/snack.service';
import { Spy } from 'src/app/test';
import { ProjectFormComponent } from './project-form.component';


describe('ProjectFormComponent', () => {
  let component: ProjectFormComponent;
  let fixture: ComponentFixture<ProjectFormComponent>;

  const projectFacadeSpy = jasmine.createSpyObj(
    'ProjectFacadeService',
    ['createProject', 'renameProject']
  );

  const formBuilderSpy = new FormBuilder();
  const dialogRefSpy = Spy.dialogRef();
  const routerSpy = Spy.router();
  const snackServiceSpy = Spy.snackService();

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ ProjectFormComponent ],
      imports: [ FormsModule ],
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
    component.ngOnInit
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should not accept an empty form', async () => {
    component.submit();
    expect(projectFacadeSpy.createProject).not.toHaveBeenCalled();
    expect(projectFacadeSpy.renameProject).not.toHaveBeenCalled();
  });
});
