import { HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { DataSourceView } from 'src/app/api/models/data-source-view';
import { ProjectView } from 'src/app/api/models/project-view';
import { TableCountsWrite } from 'src/app/api/models/table-counts-write';
import { ProjectService } from 'src/app/api/services';
import { Snack } from 'src/app/service/constants';
import { ActiveProjectService } from '../service/active-project.service';

@Component({
  selector: 'app-export',
  templateUrl: './export.component.html',
  styleUrls: ['./export.component.scss']
})
export class ExportComponent implements OnInit {

  project: ProjectView;
  tableCounts: TableCountsWrite;
  outputChoice: DataSourceView | string;

  private unsubscribe$ = new Subject();

  constructor(
    private activeProject: ActiveProjectService,
    private projectService: ProjectService,
    private snackBar: MatSnackBar
  ) { }

  ngOnInit(): void {
    this.activeProject.project$
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe((project) => this.project = project);
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  tableCountsChanged(tableCounts: TableCountsWrite) {
    this.tableCounts = tableCounts;
  }

  outputChoiceChanged(outputChoice: DataSourceView | string) {
    this.outputChoice = outputChoice;
  }

  generate() {
    this.projectService.postApiProjectIdExportResponse({
      tableCounts: this.tableCounts,
      mimeType: 'application/json',
      id: this.project.id
    }).subscribe(
      (response) => this.downloadBlob(response.body, this.fileName(response.headers)),
      () => this.snackBar.open('Something went wrong', Snack.OK, Snack.CONFIG)
    );
  }

  private fileName(headers: HttpHeaders): string {
    const contentDisposition = headers.get('Content-Disposition');
    const regex = /filename=([^;]+)/;
    try {
      return regex.exec(contentDisposition)[1];
    } catch {
      return 'export.txt';
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
