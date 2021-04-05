import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { ProjectView } from 'src/app/api/models/project-view';
import { TableCreate } from 'src/app/api/models/table-create';
import { TableView } from 'src/app/api/models/table-view';
import { TableService } from 'src/app/api/services';
import { ActiveProjectService } from './active-project.service';

@Injectable()
export class TableFacadeService {

  constructor(
    private activeProject: ActiveProjectService,
    private tableService: TableService
  ) { }

  /**
   * Create a table via the API and update the active project state.
   * 
   * @param table - The table to be created
   * @returns Observable of the created table
   */
  createTable(table: TableCreate): Observable<TableView> {
    return this.tableService.postApiTable(table)
      .pipe(
        tap((newTable) => this.activeProject.addTable(newTable))
      );
  }

  /**
   * Delete a table via the API and update the active project state.
   * 
   * @param tableId - The ID of the table to be deleted
   * @returns Observable of the new project state
   */
  deleteTable(tableId: number): Observable<ProjectView> {
    return this.tableService.deleteApiTableId(tableId)
      .pipe(
        tap((project) => this.activeProject.nextProject(project))
      );
  }
}
