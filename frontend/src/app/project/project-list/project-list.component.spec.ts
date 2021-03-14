import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { MatDialog } from '@angular/material/dialog';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { Spy } from 'src/app/test';

import { ProjectListComponent } from './project-list.component';

describe('ProjectListComponent', () => {
  let component: ProjectListComponent;
  let fixture: ComponentFixture<ProjectListComponent>;

  const dialogSpy = Spy.matDialog();
  const projectFacadeSpy = Spy.projectFacadeObservableOnly();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProjectListComponent ],
      providers: [
        {provide: MatDialog, useValue: dialogSpy},
        {provide: ProjectFacadeService, useValue: projectFacadeSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProjectListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should subscribe to project list', () => {
    component.ngOnInit();
    expect(component.projects).toBeTruthy();
  });
});
