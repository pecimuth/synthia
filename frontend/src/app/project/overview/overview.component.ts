import { Component, OnInit } from '@angular/core';
import { ProjectService } from 'src/app/api/services';
import { ActiveProjectService } from '../service/active-project.service';
import { ProjectView } from 'src/app/api/models/project-view';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';

const config = {
  duration: 2000
};

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss']
})
export class OverviewComponent implements OnInit {

  project: ProjectView;
  private unsubscribe$ = new Subject();

  constructor(
    private projectService: ProjectService,
    private projectFacade: ProjectFacadeService,
    private activeProject: ActiveProjectService,
    private snackBar: MatSnackBar
  ) { }

  ngOnInit(): void {
    this.activeProject.project$
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe((project) => this.project = project);
  }

  onCreateMock() {
    this.projectService
      .postApiProjectIdCreateMockDatabase(this.project.id)
      .subscribe(
        () => {
          this.snackBar.open('Successfully created a mock database', 'OK', config);
          this.projectFacade.refreshList();
        },
        () => this.snackBar.open('Failed to create a mock database', 'OK', config)
      );
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }
}
