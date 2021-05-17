import { Component, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { catchError, debounceTime, filter, switchMap, takeUntil } from 'rxjs/operators';
import { ExportRequisitionView } from 'src/app/api/models/export-requisition-view';
import { PreviewView } from 'src/app/api/models/preview-view';
import { ProjectView } from 'src/app/api/models/project-view';
import { ProjectService } from 'src/app/api/services';
import { ActiveProjectService } from '../service/active-project.service';

/**
 * How long should we wait (in ms) before requesting the preview from the API?
 */
const DEBOUNCE_TIME_MS = 300;

@Component({
  selector: 'app-preview',
  templateUrl: './preview.component.html',
  styleUrls: ['./preview.component.scss']
})
export class PreviewComponent implements OnInit {

  /**
   * Active project.
   */
  project: ProjectView;

  /**
   * Generated preview.
   */
  preview: PreviewView;

  /**
   * Optional error message; when the generation procedure fails.
   */
  errorMessage: string;

  /**
   * Should a progress bar be shown?
   */
  showProgress = false;

  /**
   * Subject of the preview export requisition for the API.
   * 
   * Includes changes of table names, row counts, and seeds.
   * Preview is refetched on each change of the requisition
   * or change to the project.
   */
  requisition$ = new Subject<ExportRequisitionView>();

  private unsubscribe$ = new Subject();

  constructor(
    private activeProject: ActiveProjectService,
    private projectService: ProjectService
  ) { }

  ngOnInit(): void {
    this.activeProject.project$
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe((project) => this.project = project);
      
    this.requisition$
      .pipe(
        takeUntil(this.unsubscribe$),
        filter((requisition) => !!requisition),
        debounceTime(DEBOUNCE_TIME_MS),
        switchMap((requisition) => {
          this.showProgress = true;
          return this.projectService.postApiProjectIdPreview({
            id: this.project.id,
            requisition: requisition
          });
        }),
        catchError((err, caught) => {
          this.preview = null;
          if (err?.error?.message) {
            this.errorMessage = err.error.message;
          } else {
            this.errorMessage = 'An error occured';
          }
          this.showProgress = false;
          return caught;
        })
      )
      .subscribe(
        (preview) => {
          this.preview = preview;
          this.showProgress = false;
          this.errorMessage = null;
        }
      );
  }

  setRequisition(requisition: ExportRequisitionView) {
    this.requisition$.next(requisition);
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }
}
