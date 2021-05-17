import { Component, OnDestroy, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ProjectView } from 'src/app/api/models/project-view';
import { ProjectFormComponent } from 'src/app/dialog/project-form/project-form.component';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { SnackService } from 'src/app/service/snack.service';

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
    private dialog: MatDialog,
    private snackService: SnackService
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
    this.dialog.open(ProjectFormComponent);
  }

  /**
   * Delete the project via the API and in the client's list.
   * 
   * @param project - The project to be deleted
   */
  deleteProject(project: ProjectView) {
    this.projectFacade.deleteProject(project.id)
      .subscribe(
        (msg) => this.snackService.snack(msg.message),
        (err) => this.snackService.errorIntoSnack(err)
      );
  }

  /**
   * Open the edit project dialog.
   * 
   * @param project - The project to be edited
   */
  editProject(project: ProjectView) {
    const config = {
      data: project
    };
    this.dialog.open(ProjectFormComponent, config);
  }
}
