import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { ProjectListView } from '../api/models/project-list-view';
import { ProjectView } from '../api/models/project-view';
import { ProjectService } from '../api/services';

@Injectable({
  providedIn: 'root'
})
export class ProjectFacadeService {

  _list$ = new BehaviorSubject<ProjectListView>({items: []});
  get list$() {
    return this._list$;
  }

  constructor(
    private projectService: ProjectService
  ) { }

  complete() {
    this.list$.complete();
  }

  refreshList() {
    this.projectService.getApiProjects()
      .subscribe(
        (list) => this.list$.next(list)
      );
  }
}
