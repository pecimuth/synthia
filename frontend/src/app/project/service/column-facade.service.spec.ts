import { TestBed } from '@angular/core/testing';

import { ColumnFacadeService } from './column-facade.service';

describe('ColumnFacadeService', () => {
  let service: ColumnFacadeService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ColumnFacadeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
