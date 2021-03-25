import { BreakpointObserver } from '@angular/cdk/layout';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';
import { Mock, Spy } from '../test';

import { ProjectComponent } from './project.component';
import { ActiveProjectService } from './service/active-project.service';

describe('ProjectComponent', () => {
  let component: ProjectComponent;
  let fixture: ComponentFixture<ProjectComponent>;

  const project = Mock.project();
  const activeProjectSpy = Spy.activeProjectObservableOnly();

  const activatedRouteSpy = jasmine.createSpyObj(
    'ActivatedRoute',
    [],
    {'params': of({id: project.id})}
  );
 
  const breakpoint = {matches: false};
  const breakpointObserverSpy = jasmine.createSpyObj(
    'BreakpointObserver',
    ['observe']
  );
  breakpointObserverSpy.observe.and.returnValue(of(breakpoint));

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProjectComponent ],
      providers: [
        {provide: ActiveProjectService, useValue: activeProjectSpy},
        {provide: ActivatedRoute, useValue: activatedRouteSpy},
        {provide: BreakpointObserver, useValue: breakpointObserverSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProjectComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
