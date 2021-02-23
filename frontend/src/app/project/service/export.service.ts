import { HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { DataSourceView } from 'src/app/api/models/data-source-view';
import { MessageView } from 'src/app/api/models/message-view';
import { TableCountsWrite } from 'src/app/api/models/table-counts-write';
import { DataSourceService, ProjectService } from 'src/app/api/services';
import { ActiveProjectService } from './active-project.service';

@Injectable({
  providedIn: 'root'
})
export class ExportService {

  constructor(
    private projectService: ProjectService,
    private dataSourceService: DataSourceService,
    private activeProject: ActiveProjectService
  ) { }

  export(outputChoice: DataSourceView | string,
         tableCounts: TableCountsWrite): Observable<Blob | MessageView> {
    if (typeof outputChoice === 'string') {
      return this.exportAsFile(outputChoice, tableCounts);
    } else {
      return this.exportToDataSource(outputChoice, tableCounts);
    }
  }

  private exportAsFile(outputChoice: string, tableCounts: TableCountsWrite): Observable<Blob> {
    const projectId = this.activeProject.project$.value.id;
    const params = {
      id: projectId,
      exportRequest: {
        table_counts: tableCounts,
        output_format: outputChoice as any
      }
    };

    return this.projectService.postApiProjectIdExportResponse(params)
      .pipe(
        map((response) => {
          this.downloadBlob(response.body, this.fileName(response.headers));
          return response.body;
        })
      );
  }

  private exportToDataSource(outputChoice: DataSourceView,
                             tableCounts: TableCountsWrite): Observable<MessageView> {
    const params = {
      id: outputChoice.id,
      tableCounts: tableCounts
    };
    return this.dataSourceService.postApiDataSourceDatabaseIdExport(params);
  }

  private fileName(headers: HttpHeaders): string {
    const contentDisposition = headers.get('Content-Disposition');
    const regex = /filename=([^;]+)/;
    try {
      return regex.exec(contentDisposition)[1];
    } catch {
      return 'export';
    }
  }

  private downloadBlob(blob: Blob, fileName: string) {
    const anchor = document.createElement('a');
    anchor.href = window.URL.createObjectURL(blob);
    anchor.setAttribute('download', fileName);
    document.body.appendChild(anchor);
    anchor.click();
  }
}
