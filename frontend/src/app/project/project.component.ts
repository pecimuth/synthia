import { Component, OnInit, OnDestroy } from '@angular/core';
import { ProjectView } from '../api/models/project-view';
import { ActivatedRoute } from '@angular/router';
import { Observable, Subject } from 'rxjs';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { map, shareReplay, takeUntil } from 'rxjs/operators';
import { ActiveProjectService } from './service/active-project.service'

@Component({
  selector: 'app-project',
  templateUrl: './project.component.html',
  styleUrls: ['./project.component.scss']
})
export class ProjectComponent implements OnInit, OnDestroy {

  /**
   * Observable of changes to the view area.
   * 
   * If the device is a handset, we should show a compact view.
   */
  isHandset$: Observable<boolean>;

  /**
   * Active project.
   */
  project: ProjectView;

  private unsubscribe$ = new Subject();

  constructor(
    private breakpointObserver: BreakpointObserver,
    private activatedRoute: ActivatedRoute,
    private activeProject: ActiveProjectService
  ) { }

  ngOnInit(): void {
    this.activatedRoute.params
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe((params) => {
        this.activeProject.projectId = parseInt(params.id);
      });
    this.activeProject.project$
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe((project) => this.project = project);
    this.isHandset$ = this.breakpointObserver.observe(Breakpoints.Handset)
      .pipe(
        takeUntil(this.unsubscribe$),
        map(result => result.matches),
        shareReplay()
      );
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }
}
