import { Injectable, OnDestroy } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { ProjectListView } from '../api/models/project-list-view';
import { ProjectView } from '../api/models/project-view';
import { ProjectService } from '../api/services';

@Injectable({
  providedIn: 'root'
})
export class ProjectFacadeService implements OnDestroy {

  _list$ = new BehaviorSubject<ProjectListView>({items: []});
  get list$() {
    return this._list$;
  }

  constructor(
    private projectService: ProjectService
  ) { }

  ngOnDestroy() {
    this.list$.complete();
  }

  refreshList() {
    this.projectService.getApiProjects()
      .subscribe(
        (list) => this.list$.next(list)
      );
  }

  createProject(name: string): Observable<ProjectView> {
    return this.projectService
      .postApiProject(name)
      .pipe(
        tap((project) => {
          const list = this._list$.value;
          this._list$.next({
            items: [...list.items, project]
          });
        })
      );
  }
}
