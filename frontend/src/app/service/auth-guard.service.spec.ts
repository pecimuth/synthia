import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { Spy } from '../test';
import { AuthFacadeService } from './auth-facade.service';

import { AuthGuardService } from './auth-guard.service';

describe('AuthGuardService', () => {
  let service: AuthGuardService;

  const authFacadeSpy = Spy.authFacadeObservableOnly();
  const routerSpy = Spy.router();

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {provide: AuthFacadeService, useValue: authFacadeSpy},
        {provide: Router, useValue: routerSpy}
      ]
    });
    service = TestBed.inject(AuthGuardService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
