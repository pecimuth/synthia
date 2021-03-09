import { Component, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { DataSourceView } from 'src/app/api/models/data-source-view';
import { ExportRequisitionView } from 'src/app/api/models/export-requisition-view';
import { ProjectView } from 'src/app/api/models/project-view';
import { SnackService } from 'src/app/service/snack.service';
import { ActiveProjectService } from '../service/active-project.service';
import { ExportService } from '../service/export.service';

@Component({
  selector: 'app-export',
  templateUrl: './export.component.html',
  styleUrls: ['./export.component.scss']
})
export class ExportComponent implements OnInit {

  project: ProjectView;
  requisition: ExportRequisitionView;
  outputChoice: DataSourceView | string | null;

  showProgress = false;
  private unsubscribe$ = new Subject();

  constructor(
    private activeProject: ActiveProjectService,
    private exportService: ExportService,
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

  requisitionChanged(requisition: ExportRequisitionView) {
    this.requisition = requisition;
  }

  outputChoiceChanged(outputChoice: DataSourceView | string) {
    this.outputChoice = outputChoice;
  }

  generate() {
    this.showProgress = true;
    this.exportService.export(this.outputChoice, this.requisition)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(
        () => {
          this.snackService.snack('Export completed');
          this.showProgress = false;
        },
        (err) => {
          this.snackService.errorIntoSnack(err);
          this.showProgress = false;
        }
      );
  }
}
