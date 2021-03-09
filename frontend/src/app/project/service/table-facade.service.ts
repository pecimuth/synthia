import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { ProjectView } from 'src/app/api/models/project-view';
import { TableCreate } from 'src/app/api/models/table-create';
import { TableView } from 'src/app/api/models/table-view';
import { TableService } from 'src/app/api/services';
import { ActiveProjectService } from './active-project.service';

@Injectable({
  providedIn: 'root'
})
export class TableFacadeService {

  constructor(
    private activeProject: ActiveProjectService,
    private tableService: TableService
  ) { }

  createTable(table: TableCreate): Observable<TableView> {
    return this.tableService.postApiTable(table)
      .pipe(
        tap((newTable) => this.activeProject.addTable(newTable))
      );
  }

  deleteTable(tableId: number): Observable<ProjectView> {
    return this.tableService.deleteApiTableId(tableId)
      .pipe(
        tap((project) => this.activeProject.project$.next(project))
      );
  }
}
