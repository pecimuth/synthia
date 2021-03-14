import { TestBed } from '@angular/core/testing';
import { ProjectService } from 'src/app/api/services';

import { ActiveProjectService } from './active-project.service';

describe('ActiveProjectService', () => {
  let service: ActiveProjectService;

  const projectServiceSpy = jasmine.createSpyObj(
    'ProjectService',
    ['getApiProjectId']
  );

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {provide: ProjectService, useValue: projectServiceSpy}
      ]
    });
    service = TestBed.inject(ActiveProjectService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
