import { TestBed } from '@angular/core/testing';
import { DataSourceService } from 'src/app/api/services';
import { Spy } from 'src/app/test';
import { ActiveProjectService } from './active-project.service';
import { BlobDownloadService } from './blob-download.service';

import { DataSourceFacadeService } from './data-source-facade.service';

describe('DataSourceFacadeService', () => {
  let service: DataSourceFacadeService;

  const activeProjectSpy = jasmine.createSpyObj(
    'ActiveProjectService',
    ['deleteDataSource', 'addDataSource', 'patchDataSource'],
    ['project$']
  );

  const dataSourceServiceSpy = jasmine.createSpyObj(
    'DataSourceService',
    [
      'postApiDataSourceIdImport',
      'deleteApiDataSourceId',
      'getApiDataSourceFileIdDownloadResponse',
      'postApiDataSourceDatabase',
      'patchApiDataSourceDatabaseId',
      'postApiDataSourceFile',
      'postApiDataSourceMockDatabase'
    ]
  );

  const blobDownloadSpy = Spy.blobDownloadService();

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {provide: ActiveProjectService, useValue: activeProjectSpy},
        {provide: DataSourceService, useValue: dataSourceServiceSpy},
        {provide: BlobDownloadService, useValue: blobDownloadSpy}
      ]
    });
    service = TestBed.inject(DataSourceFacadeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
