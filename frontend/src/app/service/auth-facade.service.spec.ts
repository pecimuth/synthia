import { TestBed } from '@angular/core/testing';
import { AuthService } from '../api/services';

import { AuthFacadeService } from './auth-facade.service';

describe('AuthFacadeService', () => {
  let service: AuthFacadeService;

  const authServiceSpy = jasmine.createSpyObj(
    'AuthService',
    ['postApiAuthLogin', 'postApiAuthRegister', 'getApiAuthUser']
  );

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {provide: AuthService, useValue: authServiceSpy}
      ]
    });
    service = TestBed.inject(AuthFacadeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
