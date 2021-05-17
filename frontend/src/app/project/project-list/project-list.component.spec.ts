import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { MatDialog } from '@angular/material/dialog';
import { MatMenuModule } from '@angular/material/menu';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { SnackService } from 'src/app/service/snack.service';
import { Spy } from 'src/app/test';
import { ProjectListComponent } from './project-list.component';


describe('ProjectListComponent', () => {
  let component: ProjectListComponent;
  let fixture: ComponentFixture<ProjectListComponent>;

  const dialogSpy = Spy.matDialog();
  const projectFacadeSpy = Spy.projectFacadeObservableOnly();
  const snackSpy = Spy.snackService();

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      imports: [MatMenuModule],
      declarations: [ ProjectListComponent ],
      providers: [
        {provide: MatDialog, useValue: dialogSpy},
        {provide: ProjectFacadeService, useValue: projectFacadeSpy},
        {provide: SnackService, useValue: snackSpy}
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
