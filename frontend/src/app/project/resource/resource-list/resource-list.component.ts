import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ProjectView } from 'src/app/api/models/project-view';
import { DatabaseSourceFormComponent } from 'src/app/dialog/database-source-form/database-source-form.component';
import { FileSourceFormComponent } from 'src/app/dialog/file-source-form/file-source-form.component';
import { SnackService } from 'src/app/service/snack.service';
import { ActiveProjectService } from '../../service/active-project.service';
import { DataSourceFacadeService } from '../../service/data-source-facade.service';

@Component({
  selector: 'app-resource-list',
  templateUrl: './resource-list.component.html',
  styleUrls: ['./resource-list.component.scss']
})
export class ResourceListComponent implements OnInit {

  /**
   * Active project.
   */
  project: ProjectView;

  private unsubscribe$ = new Subject();

  constructor(
    private activeProject: ActiveProjectService,
    private dialog: MatDialog,
    private dataSourceFacade: DataSourceFacadeService,
    private snackService: SnackService
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
   * Open the create database data source dialog.
   */
  createDatabase() {
    this.dialog.open(DatabaseSourceFormComponent);
  }

  /**
   * Open the create file data source dialog.
   */
  createFileSource() {
    this.dialog.open(FileSourceFormComponent);
  }

  /**
   * Create a mock database data source via the API.
   */
  mockDatabase() {
    this.dataSourceFacade.mockDatabase()
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(
        () => null,
        (err) => this.snackService.errorIntoSnack(err)
      );
  }
}
