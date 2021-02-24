import { Component, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { filter, switchMap, takeUntil } from 'rxjs/operators';
import { PreviewView } from 'src/app/api/models/preview-view';
import { ProjectView } from 'src/app/api/models/project-view';
import { TableCountsWrite } from 'src/app/api/models/table-counts-write';
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
            tableCounts: this.makeTableCounts()
          });
        })
      )
      .subscribe((preview) => this.preview = preview);
  }

  private makeTableCounts(): TableCountsWrite {
    const result = {};
    this.project.tables.forEach((table) => result[table.name] = N_PREVIEW_ROWS);
    return {rows_by_table_name: result};
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }
}
