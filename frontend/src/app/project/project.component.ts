import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable, Subject } from 'rxjs';
import { map, shareReplay, takeUntil } from 'rxjs/operators';
import { ProjectView } from '../api/models/project-view';
import { ActiveProjectService } from './service/active-project.service';
import { ColumnFacadeService } from './service/column-facade.service';
import { DataSourceFacadeService } from './service/data-source-facade.service';
import { ExportService } from './service/export.service';
import { GeneratorFacadeService } from './service/generator-facade.service';
import { TableFacadeService } from './service/table-facade.service';

@Component({
  selector: 'app-project',
  templateUrl: './project.component.html',
  styleUrls: ['./project.component.scss'],
  providers: [
    ActiveProjectService,
    ColumnFacadeService,
    DataSourceFacadeService,
    ExportService,
    GeneratorFacadeService,
    TableFacadeService
  ]
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
    private activeProject: ActiveProjectService,
    private generatorFacade: GeneratorFacadeService
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
    this.generatorFacade.refresh();
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }
}
