import { Component, OnInit, OnDestroy } from '@angular/core';
import { ProjectFacadeService } from '../service/project-facade.service';
import { ProjectView } from '../api/models/project-view';
import { ActivatedRoute } from '@angular/router';
import { Subscription, combineLatest, Observable } from 'rxjs';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { map, shareReplay } from 'rxjs/operators';
import { ProjectService } from '../api/services';

@Component({
  selector: 'app-project',
  templateUrl: './project.component.html',
  styleUrls: ['./project.component.scss']
})
export class ProjectComponent implements OnInit, OnDestroy {

  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );
  project: ProjectView;
  private projectSub: Subscription;

  constructor(
    private breakpointObserver: BreakpointObserver,
    private projectFacade: ProjectFacadeService,
    private activatedRoute: ActivatedRoute,
    private projectService: ProjectService
  ) { }

  ngOnInit(): void {
    this.projectSub = combineLatest([
      this.activatedRoute.params,
      this.projectFacade.list$
    ]).subscribe(
      ([params, list]) => {
        const id = parseInt(params.id);
        this.project = list.items.find((item) => item.id === id);
      }
    );
  }

  ngOnDestroy() {
    if (this.projectSub) {
      this.projectSub.unsubscribe();
    }
  }

  generate() {
    this.projectService.postApiProjectIdGenerate(this.project.id).subscribe();
  }
}
