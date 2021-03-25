import { TestBed } from '@angular/core/testing';
import { ProjectService } from '../api/services';

import { ProjectFacadeService } from './project-facade.service';

describe('ProjectFacadeService', () => {
  let service: ProjectFacadeService;

  const projectServiceSpy = jasmine.createSpyObj(
    'ProjectService',
    ['getApiProjects', 'postApiProject']
  );

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {provide: ProjectService, useValue: projectServiceSpy}
      ]
    });
    service = TestBed.inject(ProjectFacadeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
