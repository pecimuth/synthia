import { Injectable, OnDestroy } from '@angular/core';
import { ProjectView } from 'src/app/api/models/project-view';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { BehaviorSubject, Subscription } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ActiveProjectService implements OnDestroy {

  project$ = new BehaviorSubject<ProjectView>(null);
  private listSub: Subscription;
  set projectId(newProjectId: number) {
    this.unsubscribe();
    // active table may not be from this project
    // therefore we invalidate it
    this.listSub = this.projectFacade.list$
      .subscribe(
        (list) => {
          const found = list.items.find((item) => item.id === newProjectId);
          this.project$.next(found);
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
  }
}
