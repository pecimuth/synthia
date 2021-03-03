import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { DataSourceDatabaseWrite } from 'src/app/api/models/data-source-database-write';
import { DataSourceView } from 'src/app/api/models/data-source-view';
import { MessageView } from 'src/app/api/models/message-view';
import { ProjectView } from 'src/app/api/models/project-view';
import { DataSourceService } from 'src/app/api/services';
import { ActiveProjectService } from './active-project.service';
import { BlobDownloadService } from './blob-download.service';

@Injectable({
  providedIn: 'root'
})
export class DataSourceFacadeService {

  constructor(
    private activeProject: ActiveProjectService,
    private dataSourceService: DataSourceService,
    private blobDownloadService: BlobDownloadService
  ) { }


  import(dataSourceId: number): Observable<ProjectView> {
    return this.dataSourceService.postApiDataSourceIdImport(dataSourceId)
      .pipe(
        tap((project) => this.activeProject.project$.next(project))
      );
  }

  delete(dataSourceId: number): Observable<MessageView> {
    return this.dataSourceService.deleteApiDataSourceId(dataSourceId)
      .pipe(
        tap(() => this.activeProject.deleteDataSource(dataSourceId))
      );
  }

  download(dataSourceId: number): Observable<Blob> {
    return this.dataSourceService.getApiDataSourceFileIdDownloadResponse(dataSourceId)
      .pipe(
        map((response) => {
          this.blobDownloadService.handleResponse(response);
          return response.body;
        })
      );
  }

  createDatabase(dataSourceDatabase: DataSourceDatabaseWrite): Observable<DataSourceView> {
    const project = this.activeProject.project$.value;
    dataSourceDatabase.project_id = project.id;

    return this.dataSourceService.postApiDataSourceDatabase(dataSourceDatabase)
      .pipe(
        tap((dataSource) => this.activeProject.addDataSource(dataSource))
      );
  }

  createFileSource(dataFile: Blob): Observable<DataSourceView> {
    const project = this.activeProject.project$.value;
    const params = {
      projectId: project.id,
      dataFile: dataFile
    }

    return this.dataSourceService.postApiDataSourceFile(params)
      .pipe(
        tap((dataSource) => this.activeProject.addDataSource(dataSource))
      );
  }

  mockDatabase(): Observable<DataSourceView> {
    const project = this.activeProject.project$.value;
    return this.dataSourceService.postApiDataSourceMockDatabase(project.id)
      .pipe(
        tap((dataSource) => this.activeProject.addDataSource(dataSource))
      );
  }
}
