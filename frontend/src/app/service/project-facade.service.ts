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

  /**
   * List of user's projects.
   */
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

  /**
   * Refresh the list of user's projects from the API.
   */
  refreshList() {
    this.projectService.getApiProjects()
      .subscribe(
        (list) => this.list$.next(list)
      );
  }

  /**
   * Create a new project via the API and add it to the list.
   * 
   * @param name - The name of the new project
   * @returns Observable of the created project
   */
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
