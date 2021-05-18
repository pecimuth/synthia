import { Component, OnDestroy, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ProjectView } from 'src/app/api/models/project-view';
import { TableView } from 'src/app/api/models/table-view';
import { ActiveProjectService } from '../../service/active-project.service';
import { TableFormComponent } from '../table-form/table-form.component';

@Component({
  selector: 'app-table-list',
  templateUrl: './table-list.component.html',
  styleUrls: ['./table-list.component.scss']
})
export class TableListComponent implements OnInit, OnDestroy {

  /**
   * Active project.
   */
  project: ProjectView;

  private unsubscribe$ = new Subject();

  constructor(
    private activeProject: ActiveProjectService,
    private dialog: MatDialog
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

  /**
   * Open the create table dialog.
   */
  createTable() {
    this.dialog.open(TableFormComponent);
  }

  trackById = (index: number, item: TableView) => item.id;
}
