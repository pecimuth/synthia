import { TestBed } from '@angular/core/testing';

import { GeneratorFacadeService } from './generator-facade.service';

describe('GeneratorFacadeService', () => {
  let service: GeneratorFacadeService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GeneratorFacadeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
