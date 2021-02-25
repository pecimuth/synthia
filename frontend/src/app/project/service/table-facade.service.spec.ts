import { TestBed } from '@angular/core/testing';

import { TableFacadeService } from './table-facade.service';

describe('TableFacadeService', () => {
  let service: TableFacadeService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TableFacadeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
