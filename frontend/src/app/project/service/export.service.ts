import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { DataSourceView } from 'src/app/api/models/data-source-view';
import { ExportRequisitionView } from 'src/app/api/models/export-requisition-view';
import { MessageView } from 'src/app/api/models/message-view';
import { DataSourceService, ProjectService } from 'src/app/api/services';
import { ActiveProjectService } from './active-project.service';
import { BlobDownloadService } from './blob-download.service';

@Injectable()
export class ExportService {

  constructor(
    private projectService: ProjectService,
    private dataSourceService: DataSourceService,
    private activeProject: ActiveProjectService,
    private blobDownloadService: BlobDownloadService
  ) { }

  /**
   * Export the project to a data source or start a file download.
   * 
   * @param outputChoice - Where should the result go (database data source,
   * output file driver name, saved project)
   * @param requisition - The requested tables, row counts and seeds
   * @returns Observable of the downloaded file blob or status message
   */
  export(outputChoice: DataSourceView | string | null,
         requisition: ExportRequisitionView): Observable<Blob | MessageView> {
    if (outputChoice === null) {
      return this.saveProjectFile(requisition);
    }
    else if (typeof outputChoice === 'string') {
      return this.exportAsFile(outputChoice, requisition);
    } else {
      return this.exportToDataSource(outputChoice, requisition);
    }
  }

  private exportAsFile(outputChoice: string, requisition: ExportRequisitionView): Observable<Blob> {
    const projectId = this.activeProject.project$.value.id;
    const params = {
      id: projectId,
      requisition: {
        rows: requisition.rows,
        driver_name: outputChoice as any
      }
    };

    return this.projectService.postApiProjectIdExportResponse(params)
      .pipe(
        map((response) => {
          this.blobDownloadService.handleResponse(response);
          return response.body;
        })
      );
  }

  private saveProjectFile(requisition: ExportRequisitionView): Observable<Blob> {
    const projectId = this.activeProject.project$.value.id;
    const params = {
      id: projectId,
      requisition: requisition
    };

    return this.projectService.postApiProjectIdSaveResponse(params)
      .pipe(
        map((response) => {
          this.blobDownloadService.handleResponse(response);
          return response.body;
        })
      );
  }

  private exportToDataSource(outputChoice: DataSourceView,
                             requisition: ExportRequisitionView): Observable<MessageView> {
    const params = {
      id: outputChoice.id,
      requisition: requisition
    };
    return this.dataSourceService.postApiDataSourceDatabaseIdExport(params);
  }
}
