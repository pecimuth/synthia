import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ProjectView } from 'src/app/api/models/project-view';
import { DatabaseSourceFormComponent } from 'src/app/dialog/database-source-form/database-source-form.component';
import { FileSourceFormComponent } from 'src/app/dialog/file-source-form/file-source-form.component';
import { ActiveProjectService } from '../../service/active-project.service';

@Component({
  selector: 'app-resource-list',
  templateUrl: './resource-list.component.html',
  styleUrls: ['./resource-list.component.scss']
})
export class ResourceListComponent implements OnInit {

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

  createDatabase() {
    this.dialog.open(DatabaseSourceFormComponent);
  }

  createFileSource() {
    this.dialog.open(FileSourceFormComponent);
  }
}
