import { TestBed, waitForAsync } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { of, Subject } from 'rxjs';
import { ProjectView } from './api/models';
import { AppComponent } from './app.component';
import { AuthFacadeService } from './service/auth-facade.service';
import { ProjectFacadeService } from './service/project-facade.service';
import { Mock } from './test';

describe('AppComponent', () => {

  const user = Mock.user();
  const authFacadeServiceSpy = jasmine.createSpyObj(
    'AuthFacadeService',
    ['refresh'],
    {'user$': of(user)}
  );

  const project$ = new Subject<ProjectView>();
  const projectFacadeServiceSpy = jasmine.createSpyObj(
    'ProjectFacadeService',
    ['refresh'],
    {'project$': project$}
  );

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule
      ],
      declarations: [
        AppComponent
      ],
      providers: [
        {provide: AuthFacadeService, useValue: authFacadeServiceSpy},
        {provide: ProjectFacadeService, useValue: projectFacadeServiceSpy}
      ]
    }).compileComponents();
  }));

  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });
});
