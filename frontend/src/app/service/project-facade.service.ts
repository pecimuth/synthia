import { Injectable, OnDestroy } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { ProjectListView } from '../api/models/project-list-view';
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
}
