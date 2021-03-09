import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { ColumnCreate } from 'src/app/api/models/column-create';
import { ColumnView } from 'src/app/api/models/column-view';
import { GeneratorSettingView } from 'src/app/api/models/generator-setting-view';
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

  setColumnGeneratorSetting(tableId: number,
                            columnId: number,
                            setting: GeneratorSettingView): Observable<ColumnView> {
    const params = {
      id: columnId,
      column: {
        generator_setting_id: setting.id
      }
    };
    return this.columnService.patchApiColumnId(params)
      .pipe(
        tap((newColumn) => this.activeProject.patchColumn(tableId, newColumn))
      );
  }

  createColumn(column: ColumnCreate): Observable<ColumnView> {
    return this.columnService.postApiColumn(column)
      .pipe(
        tap((newColumn) => this.activeProject
          .addColumn(column.table_id, newColumn))
      );
  }

  deleteColumn(columnId: number): Observable<ProjectView> {
    return this.columnService.deleteApiColumnId(columnId)
      .pipe(
        tap((project) => this.activeProject.project$.next(project))
      );
  }
}
