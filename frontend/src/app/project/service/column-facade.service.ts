import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { ColumnWrite } from 'src/app/api/models';
import { ColumnCreate } from 'src/app/api/models/column-create';
import { ColumnView } from 'src/app/api/models/column-view';
import { ProjectView } from 'src/app/api/models/project-view';
import { ColumnService } from 'src/app/api/services';
import { ActiveProjectService } from './active-project.service';

@Injectable({
  providedIn: 'root'
})
export class ColumnFacadeService {

  constructor(
    private columnService: ColumnService,
    private activeProject: ActiveProjectService
  ) { }

  /**
   * Assign a setting to a column via the API and update the active project.
   * 
   * @param tableId - The ID of the table containing the setting
   * @param columnId - The ID of the column
   * @param settingId - The ID of the setting
   * @returns Observable of the updated column
   */
  setColumnGeneratorSetting(tableId: number,
                            columnId: number,
                            settingId: number): Observable<ColumnView> {
    const column = {
      generator_setting_id: settingId
    };
    return this.patchColumn(tableId, columnId, column);
  }

  /**
   * Create a column via the API and update the active project.
   * 
   * @param column - The column to be created
   * @returns Observable of the created column
   */
  createColumn(column: ColumnCreate): Observable<ColumnView> {
    return this.columnService.postApiColumn(column)
      .pipe(
        tap((newColumn) => this.activeProject
          .addColumn(column.table_id, newColumn))
      );
  }

  /**
   * Delete a column via the API and update the active project.
   * 
   * @param columnId - The ID of the column to be deleted
   * @returns Observable of the updated project state
   */
  deleteColumn(columnId: number): Observable<ProjectView> {
    return this.columnService.deleteApiColumnId(columnId)
      .pipe(
        tap((project) => this.activeProject.nextProject(project))
      );
  }

  /**
   * Patch a column via the API and update the active project.
   * 
   * @param tableId - The ID of the table containing the column
   * @param columnId - The ID of the column
   * @param column - The updated column content
   * @returns Observable of the updated column
   */
  patchColumn(tableId: number, columnId: number, column: ColumnWrite): Observable<ColumnView> {
    const params = {
      id: columnId,
      column: column
    };
    return this.columnService.patchApiColumnId(params)
      .pipe(
        tap((newColumn) => this.activeProject.patchColumn(tableId, newColumn))
      );
  }
}
