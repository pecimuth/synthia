import { Component, OnDestroy, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute } from '@angular/router';
import { config, Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ProjectView } from 'src/app/api/models/project-view';
import { ProjectService } from 'src/app/api/services';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { ActiveProjectService } from '../service/active-project.service';

@Component({
  selector: 'app-table-list',
  templateUrl: './table-list.component.html',
  styleUrls: ['./table-list.component.scss']
})
export class TableListComponent implements OnInit, OnDestroy {

  project: ProjectView;
  private unsubscribe$ = new Subject();

  constructor(
    private activeProject: ActiveProjectService,
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
}
