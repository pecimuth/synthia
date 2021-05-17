import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { DataSourceDatabaseCreate } from 'src/app/api/models/data-source-database-create';
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

  /**
   * Import schema from a data source via the API and update the project state.
   * 
   * @param dataSourceId - The ID of the data source to be imported from
   * @returns Observable of the new project schema
   */
  import(dataSourceId: number): Observable<ProjectView> {
    return this.dataSourceService.postApiDataSourceIdImport(dataSourceId)
      .pipe(
        tap((project) => this.activeProject.nextProject(project))
      );
  }

  /**
   * Delete a data source via the API and update the active project state.
   * 
   * @param dataSourceId - The ID of the data source to be deleted
   * @returns Observable of the operation status message
   */
  delete(dataSourceId: number): Observable<MessageView> {
    return this.dataSourceService.deleteApiDataSourceId(dataSourceId)
      .pipe(
        tap(() => this.activeProject.deleteDataSource(dataSourceId))
      );
  }

  /**
   * Start a download of a data source file.
   * 
   * @param dataSourceId - The ID of the data source to be downloaded
   * @returns Observable of the file blob
   */
  download(dataSourceId: number): Observable<Blob> {
    return this.dataSourceService.getApiDataSourceFileIdDownloadResponse(dataSourceId)
      .pipe(
        map((response) => {
          this.blobDownloadService.handleResponse(response);
          return response.body;
        })
      );
  }

  /**
   * Create a new database datasource via the API and update the active project.
   * 
   * @param dataSourceDatabase - The data source to be created
   * @returns Observable of the created data source
   */
  createDatabase(dataSourceDatabase: DataSourceDatabaseCreate): Observable<DataSourceView> {
    const project = this.activeProject.project$.value;
    dataSourceDatabase.project_id = project.id;

    return this.dataSourceService.postApiDataSourceDatabase(dataSourceDatabase)
      .pipe(
        tap((dataSource) => this.activeProject.addDataSource(dataSource))
      );
  }

  /**
   * Patch a data source via the API and update the active project state.
   * 
   * @param dataSourceId - The ID od the data source to be patched
   * @param dataSource - The content of the patch
   * @returns Observable of the patched data source.
   */
  patchDatabase(dataSourceId: number, dataSource: DataSourceDatabaseWrite): Observable<DataSourceView> {
    const params = {
      id: dataSourceId,
      dataSourceDatabase: dataSource
    };
    return this.dataSourceService.patchApiDataSourceDatabaseId(params)
      .pipe(
        tap((dataSource) => this.activeProject.patchDataSource(dataSource))
      );
  }

  /**
   * Create a file data source via the API and update the active project state.
   * 
   * @param dataFile - The file content
   * @returns Observable of the created data source
   */
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

  /**
   * Create a mock database via the API and update the active project state.
   * 
   * @returns Observable of the created database
   */
  mockDatabase(): Observable<DataSourceView> {
    const project = this.activeProject.project$.value;
    return this.dataSourceService.postApiDataSourceMockDatabase(project.id)
      .pipe(
        tap((dataSource) => this.activeProject.addDataSource(dataSource))
      );
  }
}
