import { Component, OnInit, OnDestroy } from '@angular/core';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { ProjectView } from 'src/app/api/models/project-view';
import { Subject } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { CreateProjectFormComponent } from 'src/app/dialog/create-project-form/create-project-form.component';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-project-list',
  templateUrl: './project-list.component.html',
  styleUrls: ['./project-list.component.scss']
})
export class ProjectListComponent implements OnInit, OnDestroy {

  projects: ProjectView[];
  private unsubscribe$ = new Subject();

  constructor(
    private projectFacade: ProjectFacadeService,
    private dialog: MatDialog
  ) { }

  ngOnInit(): void {
    this.projectFacade.list$
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(
        (projects) => this.projects = projects.items
      );
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }
  
  createProject() {
    this.dialog.open(CreateProjectFormComponent);
  }
}
