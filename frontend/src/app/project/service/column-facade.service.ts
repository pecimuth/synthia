import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { ColumnView } from 'src/app/api/models/column-view';
import { GeneratorSettingView } from 'src/app/api/models/generator-setting-view';
import { TableView } from 'src/app/api/models/table-view';
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

  setColumnGeneratorSetting(table: TableView,
                            column: ColumnView,
                            setting: GeneratorSettingView): Observable<ColumnView> {
    const params = {
      id: column.id,
      column: {
        ...column,
        generator_setting_id: setting.id
      }
    };
    delete params.column.id;
    delete params.column.generator_setting;
    return this.columnService.patchApiColumnId(params)
      .pipe(
        tap((column) => this.activeProject.patchColumn(table.id, column))
      );
  }
}
