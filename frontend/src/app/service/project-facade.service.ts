import { Injectable, OnDestroy } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { filter, map, take, tap } from 'rxjs/operators';
import { MessageView } from '../api/models';
import { ProjectView } from '../api/models/project-view';
import { ProjectService } from '../api/services';

@Injectable({
  providedIn: 'root'
})
export class ProjectFacadeService implements OnDestroy {

  /**
   * List of user's projects.
   */
  projects$ = new BehaviorSubject<ProjectView[]>(null);

  constructor(
    private projectService: ProjectService
  ) { }

  ngOnDestroy() {
    this.projects$.complete();
  }

  /**
   * Refresh the list of user's projects from the API.
   */
  refresh() {
    this.projectService.getApiProjects()
      .subscribe(
        (projects) => this.projects$.next(projects.items)
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
          const projects = this.projects$.value ?? [];
          this.projects$.next([
            ...projects,
            project
          ]);
        })
      );
  }

  /**
   * Replace a project instance in the list of cached projects.
   * 
   * @param project - The patched project
   */
  patchProject(project: ProjectView) {
    const projects = this.projects$.value ?? [];
    const patchedProjects = projects.map(
      (other) => other.id === project.id ? project : other
    );
    this.projects$.next(patchedProjects);
  }

  /**
   * Find a project in the project list by ID.
   * Returns at most once. If the projects are not loaded yet,
   * wait for it.
   * 
   * @param projectId - The ID of the requested project
   * @returns Observable of a project, returning at most once
   */
  findById(projectId: number): Observable<ProjectView> {
    return this.projects$.pipe(
      filter((projects) => !!projects),
      take(1),
      map((projects) => projects.find((project) => project.id === projectId))
    );
  }

  /**
   * Delete a project via the API and update the list of cached projects.
   * 
   * @param projectId - The ID of the project to be deleted
   * @returns Observable of the operation status message
   */
  deleteProject(projectId: number): Observable<MessageView> {
    return this.projectService.deleteApiProjectId(projectId)
      .pipe(
        tap(() => {
          let projects = this.projects$.value ?? [];
          projects = projects.filter((project) => project.id !== projectId);
          this.projects$.next(projects);
        })
      );
  }

  /**
   * Change the name of a project via the API and update the list of cached projects.
   * 
   * @param projectId - The ID of the project to be renamed
   * @param newName - The new name of the project
   * @returns Observable of the patched project
   */
  renameProject(projectId: number, newName: string): Observable<ProjectView> {
    const params = {
      id: projectId,
      project: {
        name: newName
      }
    };
    return this.projectService.patchApiProjectId(params)
      .pipe(
        tap((project) => this.patchProject(project))
      );
  }
}
