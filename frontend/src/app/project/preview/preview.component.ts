import { Component, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { filter, switchMap, takeUntil } from 'rxjs/operators';
import { ExportRequisitionWrite } from 'src/app/api/models/export-requisition-write';
import { PreviewView } from 'src/app/api/models/preview-view';
import { ProjectView } from 'src/app/api/models/project-view';
import { ProjectService } from 'src/app/api/services';
import { ActiveProjectService } from '../service/active-project.service';

const N_PREVIEW_ROWS = 5;
@Component({
  selector: 'app-preview',
  templateUrl: './preview.component.html',
  styleUrls: ['./preview.component.scss']
})
export class PreviewComponent implements OnInit {

  project: ProjectView;
  preview: PreviewView;

  private unsubscribe$ = new Subject();

  constructor(
    private activeProject: ActiveProjectService,
    private projectService: ProjectService
  ) { }

  ngOnInit(): void {
    this.activeProject.project$
      .pipe(
        takeUntil(this.unsubscribe$),
        filter((project) => !!project),
        switchMap((project) => {
          this.project = project;
          return this.projectService.postApiProjectIdPreview({
            id: project.id,
            requisition: this.makeRequisition()
          });
        })
      )
      .subscribe((preview) => this.preview = preview);
  }

  private makeRequisition(): ExportRequisitionWrite {
    const result: ExportRequisitionWrite = {
      rows: this.project.tables.map((table) => {
        return {
          table_name: table.name,
          row_count: N_PREVIEW_ROWS,
          seed: 1
        };
      })
    };
    return result;
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }
}
