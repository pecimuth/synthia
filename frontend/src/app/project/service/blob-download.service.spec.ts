import { TestBed } from '@angular/core/testing';

import { BlobDownloadService } from './blob-download.service';

describe('BlobDownloadService', () => {
  let service: BlobDownloadService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BlobDownloadService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
