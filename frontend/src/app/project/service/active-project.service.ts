import { Injectable, OnDestroy } from '@angular/core';
import { ProjectView } from 'src/app/api/models/project-view';
import { BehaviorSubject, Observable, Subscription } from 'rxjs';
import { ProjectService } from 'src/app/api/services';
import { DataSourceView } from 'src/app/api/models/data-source-view';
import { ColumnView } from 'src/app/api/models/column-view';
import { TableView } from 'src/app/api/models/table-view';
import { GeneratorSettingView } from 'src/app/api/models/generator-setting-view';
import { filter, map } from 'rxjs/operators';

type Transformer = (project: ProjectView) => ProjectView;
type TableTransformer = (table: TableView) => TableView;
type ColumnTransformer = (column: ColumnView) => ColumnView;

@Injectable({
  providedIn: 'root'
})
export class ActiveProjectService implements OnDestroy {

  project$ = new BehaviorSubject<ProjectView>(null);
  private apiSubscription: Subscription;
  set projectId(newProjectId: number) {
    this.unsubscribe();
    this.apiSubscription = this.projectService
      .getApiProjectId(newProjectId)
      .subscribe(
        (project) => this.project$.next(project)
      );
  }

  constructor(
    private projectService: ProjectService
  ) { }

  ngOnDestroy() {
    this.unsubscribe();
  }

  getTable(tableId: number): Observable<TableView> {
    return this.project$.pipe(
      filter((project) => !!project),
      map((project) => project.tables.find((other) => other.id === tableId))
    );
  }

  getTableColumn(tableId: number, columnId: number): Observable<[TableView, ColumnView]> {
    return this.getTable(tableId).pipe(
      map((table) => [
        table, 
        table.columns.find((other) => other.id === columnId)
      ])
    );
  }

  private unsubscribe() {
    if (this.apiSubscription) {
      this.apiSubscription.unsubscribe();
    }
  }

  private transform(transformer: Transformer) {
    const project = this.project$.value;
    if (project === null) {
      return;
    }
    const newProject = transformer(project);
    this.project$.next(newProject);
  }

  private transformTable(tableId: number, transformer: TableTransformer) {
    const projectTransformer: Transformer = (project) => {
      const newTables = project.tables
        .map((table) => {
          if (table.id !== tableId) {
            return table;
          }
          return transformer(table);
        });
      return {
        ...project,
        tables: newTables
      };
    }
    this.transform(projectTransformer);
  }

  private transformColumn(tableId: number, columnId: number, transformer: ColumnTransformer) {
    const tableTransformer: TableTransformer = (table) => {
      const newColumns = table.columns
        .map((column) => {
          if (column.id !== columnId) {
            return column;
          }
          return transformer(column);
        })
      return {
        ...table,
        columns: newColumns
      };
    };
    this.transformTable(tableId, tableTransformer);
  }

  addDataSource(dataSource: DataSourceView) {
    this.transform(
      (project) => {
        return {
          ...project,
          data_sources: [...project.data_sources, dataSource]
        };
      }
    );
  }

  patchDataSource(dataSource: DataSourceView) {
    const transformDataSource = (other: DataSourceView) => {
      if (other.id !== dataSource.id) {
        return other;
      }
      return dataSource;
    };
    const transformer: Transformer = (project) => {
      return {
        ...project,
        data_sources: project.data_sources.map(transformDataSource)
      };
    };
    this.transform(transformer);
  }

  deleteDataSource(dataSourceId: number) {
    this.transform(
      (project) => {
        return {
          ...project,
          data_sources: project.data_sources
            .filter((other) => other.id !== dataSourceId)
        };
      }
    );
  }

  addTable(table: TableView) {
    this.transform(
      (project) => {
        return {
          ...project,
          tables: [...project.tables, table]
        };
      }
    );
  }

  addColumn(tableId: number, column: ColumnView) {
    const transformTable: TableTransformer = (table) => {
      return {
        ...table,
        columns: [...table.columns, column]
      };
    };
    this.transformTable(tableId, transformTable);
  }

  patchColumn(tableId: number, column: ColumnView) {
    const transform: ColumnTransformer = () => column;
    this.transformColumn(tableId, column.id, transform);
  }

  patchGeneratorSetting(tableId: number, setting: GeneratorSettingView) {
    const transformColumn: ColumnTransformer = (column) => {
      if (column.generator_setting?.id !== setting.id) {
        return column;
      }
      return {
        ...column,
        generator_setting: setting
      };
    };
    const transformTable: TableTransformer = (table) => {
      const newSettings = table.generator_settings
        .map((other) => {
          if (other.id !== setting.id) {
            return other;
          }
          return setting;
        });
      return {
        ...table,
        columns: table.columns.map(transformColumn),
        generator_settings: newSettings
      };
    };
    this.transformTable(tableId, transformTable);
  }

  addGeneratorSetting(tableId: number, columnId: number, setting: GeneratorSettingView) {
    const transformColumn: ColumnTransformer = (column) => {
      if (column.id !== columnId) {
        return column;
      }
      return {
        ...column,
        generator_setting: setting
      };
    };
    const transformTable: TableTransformer = (table) => {
      return {
        ...table,
        columns: table.columns.map(transformColumn),
        generator_settings: [...table.generator_settings, setting]
      };
    };
    this.transformTable(tableId, transformTable);
  }

  deleteGeneratorSetting(tableId: number, settingId: number) {
    const transformColumn: ColumnTransformer = (column) => {
      if (column.generator_setting?.id !== settingId) {
        return column;
      }
      return {
        ...column,
        generator_setting: null
      };
    };
    const transformTable: TableTransformer = (table) => {
      const newSettings = table.generator_settings
        .filter((other) => other.id !== settingId);
      return {
        ...table,
        columns: table.columns.map(transformColumn),
        generator_settings: newSettings
      };
    };
    this.transformTable(tableId, transformTable);
  }
}
