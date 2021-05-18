import { Injectable, OnDestroy } from '@angular/core';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
import { filter, map, takeUntil } from 'rxjs/operators';
import { ColumnView } from 'src/app/api/models/column-view';
import { DataSourceView } from 'src/app/api/models/data-source-view';
import { GeneratorSettingView } from 'src/app/api/models/generator-setting-view';
import { ProjectView } from 'src/app/api/models/project-view';
import { TableView } from 'src/app/api/models/table-view';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';

type ProjectTransformer = (project: ProjectView) => ProjectView;
type TableTransformer = (table: TableView) => TableView;
type ColumnTransformer = (column: ColumnView) => ColumnView;

@Injectable({
  providedIn: 'root'
})
export class ActiveProjectService implements OnDestroy {

  /**
   * Currently active project.
   */
  project$ = new BehaviorSubject<ProjectView>(null);

  private unsubscribe$ = new Subject();

  /**
   * Get the ID of the currently active project.
   */
  get projectId(): number {
    const project = this.project$.value;
    if (project) {
      return project.id;
    }
    return undefined;
  }

  /**
   * Set active project ID.
   */
  set projectId(newProjectId: number) {
    this.unsubscribe$.next();
    this.projectFacade
      .findById(newProjectId)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(
        (project) => this.project$.next(project)
      );
  }

  constructor(
    private projectFacade: ProjectFacadeService
  ) { }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  /**
   * Returns an observable of a table by ID in the active project.
   * 
   * @param tableId - ID of the table to be observed
   * @returns Observable of the table by ID
   */
  getTable(tableId: number): Observable<TableView> {
    return this.project$.pipe(
      filter((project) => !!project),
      map((project) => project.tables.find((other) => other.id === tableId))
    );
  }

  /**
   * Returns an observable of a table and its column by IDs
   * in the active project.
   * 
   * @param tableId - ID of the table containing the column
   * @param columnId - ID of the column
   * @returns Obervable of table and column
   */
  getTableColumn(tableId: number, columnId: number): Observable<[TableView, ColumnView]> {
    return this.getTable(tableId).pipe(
      map((table) => [
        table, 
        table.columns.find((other) => other.id === columnId)
      ])
    );
  }

  /**
   * Replace the project instance by a new instance.
   * Also replaces the project in the project facade's list.
   * 
   * @param project - The patche project instance
   */
  nextProject(project: ProjectView) {
    this.projectFacade.patchProject(project);
    this.project$.next(project);
  }

  /**
   * Apply a function to the active project state creating new state.
   * 
   * @param transformer - The function returning new project state
   */
  private transformProject(transformer: ProjectTransformer) {
    const project = this.project$.value;
    if (project === null) {
      return;
    }
    const newProject = transformer(project);
    this.nextProject(newProject);
  }

  /**
   * Apply a function to a table creating new project state.
   * 
   * @param tableId - The ID of the table to be transformed
   * @param transformer - The function returning new table state
   */
  private transformTable(tableId: number, transformer: TableTransformer) {
    const projectTransformer: ProjectTransformer = (project) => {
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
    this.transformProject(projectTransformer);
  }

  /**
   * Apply a function to a column creating new project state.
   * 
   * @param tableId - The ID of the table containing the column
   * @param columnId - The ID of the column to be transformed
   * @param transformer - The function returning new column state
   */
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

  /**
   * Append a new data source to the project state.
   * 
   * @param dataSource - The data source to be appended
   */
  addDataSource(dataSource: DataSourceView) {
    this.transformProject(
      (project) => {
        return {
          ...project,
          data_sources: [...project.data_sources, dataSource]
        };
      }
    );
  }

  /**
   * Replace a data source in the project state.
   * The data sources are compared by IDs.
   * 
   * @param dataSource - The patched data source
   */
  patchDataSource(dataSource: DataSourceView) {
    const transformDataSource = (other: DataSourceView) => {
      if (other.id !== dataSource.id) {
        return other;
      }
      return dataSource;
    };
    const transformer: ProjectTransformer = (project) => {
      return {
        ...project,
        data_sources: project.data_sources.map(transformDataSource)
      };
    };
    this.transformProject(transformer);
  }

  /**
   * Delete a data source from the project state.
   * 
   * @param dataSourceId - The ID of the data source to be deleted
   */
  deleteDataSource(dataSourceId: number) {
    this.transformProject(
      (project) => {
        return {
          ...project,
          data_sources: project.data_sources
            .filter((other) => other.id !== dataSourceId)
        };
      }
    );
  }

  /**
   * Append a new table to the project state.
   * 
   * @param table - The table to be appended
   */
  addTable(table: TableView) {
    this.transformProject(
      (project) => {
        return {
          ...project,
          tables: [...project.tables, table]
        };
      }
    );
  }

  /**
   * Replace a table in the project state.
   * 
   * @param table - The table that replaces a table with the same ID
   */
  patchTable(table: TableView) {
    const transformTable: TableTransformer = (other) => table;
    this.transformTable(table.id, transformTable);
  }

  /**
   * Append a new column to a table in the project state.
   * 
   * @param tableId - The ID of the target table
   * @param column - The new column
   */
  addColumn(tableId: number, column: ColumnView) {
    const transformTable: TableTransformer = (table) => {
      return {
        ...table,
        columns: [...table.columns, column]
      };
    };
    this.transformTable(tableId, transformTable);
  }

  /**
   * Replace a column in a table in the project state
   * The columns are compared by ID.
   * 
   * @param tableId - The ID of the table containing the column
   * @param column - The column to be replaced
   */
  patchColumn(tableId: number, column: ColumnView) {
    const transform: ColumnTransformer = () => column;
    this.transformColumn(tableId, column.id, transform);
  }

  /**
   * Replace a generator setting in a table in the project state.
   * The settings are compared by ID.
   * 
   * @param tableId - The ID of the table containing the generator setting ID
   * @param setting - The patched generator setting
   */
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

  /**
   * Append a generator setting to the project state,
   * possibly assigning it to a column.
   * 
   * @param tableId - The ID of the table to which the setting belongs
   * @param columnId - The ID of an assigned column
   * @param setting - The generator setting to be appended
   */
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

  /**
   * Delete a generator setting from the project state.
   * 
   * @param tableId - The ID of the table containing the setting
   * @param settingId - The ID of the setting to be deleted
   */
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
