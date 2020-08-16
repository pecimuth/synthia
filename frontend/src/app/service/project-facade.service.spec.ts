import { TestBed } from '@angular/core/testing';

import { ProjectFacadeService } from './project-facade.service';

describe('ProjectFacadeService', () => {
  let service: ProjectFacadeService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ProjectFacadeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
