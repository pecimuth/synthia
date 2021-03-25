import { TestBed, async } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { of } from 'rxjs';
import { AppComponent } from './app.component';
import { GeneratorFacadeService } from './project/service/generator-facade.service';
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

  const projectFacadeServiceSpy = jasmine.createSpyObj(
    'ProjectFacadeService',
    ['refreshList']
  );

  const generatorFacadeServiceSpy = jasmine.createSpyObj(
    'GeneratorFacadeService',
    ['refresh']
  );

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule
      ],
      declarations: [
        AppComponent
      ],
      providers: [
        {provide: AuthFacadeService, useValue: authFacadeServiceSpy},
        {provide: ProjectFacadeService, useValue: projectFacadeServiceSpy},
        {provide: GeneratorFacadeService, useValue: generatorFacadeServiceSpy}
      ]
    }).compileComponents();
  }));

  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });
});
