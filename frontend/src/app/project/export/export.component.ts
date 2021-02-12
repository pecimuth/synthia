import { Component, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { DataSourceView } from 'src/app/api/models/data-source-view';
import { ProjectView } from 'src/app/api/models/project-view';
import { TableCountsWrite } from 'src/app/api/models/table-counts-write';
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
    private activeProject: ActiveProjectService
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
}
