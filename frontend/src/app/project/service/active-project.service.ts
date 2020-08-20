import { Injectable, OnDestroy } from '@angular/core';
import { ProjectView } from 'src/app/api/models/project-view';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { BehaviorSubject, Subscription } from 'rxjs';
import { TableView } from 'src/app/api/models/table-view';
import { filter, take } from 'rxjs/operators';

@Injectable()
export class ActiveProjectService implements OnDestroy {

  project$ = new BehaviorSubject<ProjectView>(null);
  private listSub: Subscription;
  set projectId(newProjectId: number) {
    this.unsubscribe();
    // active table may not be from this project
    // therefore we invalidate it
    this.table$.next(null);
    this.listSub = this.projectFacade.list$
      .subscribe(
        (list) => {
          const found = list.items.find((item) => item.id === newProjectId);
          this.project$.next(found);
        }
      );
  }

  table$ = new BehaviorSubject<TableView>(null);
  private tableSub: Subscription;
  set tableId(newTableId: number) {
    if (this.tableSub) {
      this.tableSub.unsubscribe();
    }
    // we may need to wait for the first project
    this.tableSub = this.project$
      .pipe(
        filter((project) => !!project),
        take(1)
      )
      .subscribe(
        (project) => {
          const found = project.tables.find((item) => item.id === newTableId);
          this.table$.next(found);
        }
      );
  }

  constructor(
    private projectFacade: ProjectFacadeService
  ) { }

  ngOnDestroy() {
    this.unsubscribe();
  }

  private unsubscribe() {
    if (this.listSub) {
      this.listSub.unsubscribe();
    }
    if (this.tableSub) {
      this.tableSub.unsubscribe();
    }
  }
}
