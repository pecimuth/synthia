import { TestBed } from '@angular/core/testing';

import { DataSourceFacadeService } from './data-source-facade.service';

describe('DataSourceFacadeService', () => {
  let service: DataSourceFacadeService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DataSourceFacadeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
