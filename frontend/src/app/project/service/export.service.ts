import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { DataSourceView } from 'src/app/api/models/data-source-view';
import { ExportRequisitionWrite } from 'src/app/api/models/export-requisition-write';
import { MessageView } from 'src/app/api/models/message-view';
import { DataSourceService, ProjectService } from 'src/app/api/services';
import { ActiveProjectService } from './active-project.service';
import { BlobDownloadService } from './blob-download.service';

@Injectable({
  providedIn: 'root'
})
export class ExportService {

  constructor(
    private projectService: ProjectService,
    private dataSourceService: DataSourceService,
    private activeProject: ActiveProjectService,
    private blobDownloadService: BlobDownloadService
  ) { }

  export(outputChoice: DataSourceView | string,
         requisition: ExportRequisitionWrite): Observable<Blob | MessageView> {
    if (typeof outputChoice === 'string') {
      return this.exportAsFile(outputChoice, requisition);
    } else {
      return this.exportToDataSource(outputChoice, requisition);
    }
  }

  private exportAsFile(outputChoice: string, requisition: ExportRequisitionWrite): Observable<Blob> {
    const projectId = this.activeProject.project$.value.id;
    const params = {
      id: projectId,
      requisition: {
        rows: requisition.rows,
        driver_name: outputChoice
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

  private exportToDataSource(outputChoice: DataSourceView,
                             requisition: ExportRequisitionWrite): Observable<MessageView> {
    const params = {
      id: outputChoice.id,
      requisition: requisition
    };
    return this.dataSourceService.postApiDataSourceDatabaseIdExport(params);
  }
}
