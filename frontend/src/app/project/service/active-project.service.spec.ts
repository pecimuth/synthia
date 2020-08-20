import { TestBed } from '@angular/core/testing';

import { ActiveProjectService } from './active-project.service';

describe('ActiveProjectService', () => {
  let service: ActiveProjectService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ActiveProjectService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
