import { Component, OnDestroy, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ProjectView } from 'src/app/api/models/project-view';
import { CreateProjectFormComponent } from 'src/app/dialog/create-project-form/create-project-form.component';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';

@Component({
  selector: 'app-project-list',
  templateUrl: './project-list.component.html',
  styleUrls: ['./project-list.component.scss']
})
export class ProjectListComponent implements OnInit, OnDestroy {

  /**
   * List of user's projects.
   */
  projects: ProjectView[];

  private unsubscribe$ = new Subject();

  constructor(
    private projectFacade: ProjectFacadeService,
    private dialog: MatDialog
  ) { }

  ngOnInit(): void {
    this.projectFacade.projects$
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(
        (projects) => this.projects = projects
      );
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  /**
   * Open the create project dialog.
   */
  createProject() {
    this.dialog.open(CreateProjectFormComponent);
  }
}
