import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { Router } from '@angular/router';
import { AuthFacadeService } from 'src/app/service/auth-facade.service';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { SnackService } from 'src/app/service/snack.service';
import { Spy } from 'src/app/test';

import { LandingPageComponent } from './landing-page.component';

describe('LandingPageComponent', () => {
  let component: LandingPageComponent;
  let fixture: ComponentFixture<LandingPageComponent>;

  const authFacadeSpy = jasmine.createSpyObj(
    'AuthFacadeService',
    ['register']
  );

  const projectFacadeSpy = jasmine.createSpyObj(
    'ProjectFacadeService',
    ['createProject']
  );

  const snackServiceSpy = Spy.snackService();
  const routerSpy = Spy.router();

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ LandingPageComponent ],
      providers: [
        {provide: SnackService, useValue: snackServiceSpy},
        {provide: AuthFacadeService, useValue: authFacadeSpy},
        {provide: ProjectFacadeService, useValue: projectFacadeSpy},
        {provide: Router, useValue: routerSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LandingPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
