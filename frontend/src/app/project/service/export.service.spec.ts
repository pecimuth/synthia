import { TestBed } from '@angular/core/testing';
import { DataSourceService, ProjectService } from 'src/app/api/services';
import { Spy } from 'src/app/test';
import { ActiveProjectService } from './active-project.service';
import { BlobDownloadService } from './blob-download.service';

import { ExportService } from './export.service';

describe('ExportService', () => {
  let service: ExportService;

  const activeProjectSpy = jasmine.createSpyObj(
    'ActiveProjectService',
    [],
    ['project$']
  );

  const projectServiceSpy = jasmine.createSpyObj(
    'ProjectService',
    ['postApiProjectIdExportResponse', 'postApiProjectIdSaveResponse']
  );

  const dataSourceServiceSpy = jasmine.createSpyObj(
    'DataSourceService',
    ['postApiDataSourceDatabaseIdExport']
  );

  const blobDownloadSpy = Spy.blobDownloadService();

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {provide: ActiveProjectService, useValue: activeProjectSpy},
        {provide: ProjectService, useValue: projectServiceSpy},
        {provide: DataSourceService, useValue: dataSourceServiceSpy},
        {provide: BlobDownloadService, useValue: blobDownloadSpy}
      ]
    });
    service = TestBed.inject(ExportService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
