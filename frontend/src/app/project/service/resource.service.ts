import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DataSourceService } from 'src/app/api/services';
import { ActiveProjectService } from './active-project.service';
import { Snack } from 'src/app/service/constants';

@Injectable()
export class ResourceService {

  constructor(
    private activeProject: ActiveProjectService,
    private snackBar: MatSnackBar,
    private dataSourceService: DataSourceService
  ) { }

  private snack(message: string) {
    this.snackBar.open(message, Snack.OK, Snack.CONFIG);
  }

  import(data_source_id: number) {
    this.dataSourceService.postApiDataSourceIdImport(data_source_id)
      .subscribe(
        (project) => {
          this.snack('Successfully imported the schema')
          this.activeProject.project$.next(project);
        },
        () => this.snack('Import failed')
      );
  }

  export(data_source_id: number) {
    this.dataSourceService.postApiDataSourceDatabaseIdExport(data_source_id)
      .subscribe(
        (message) => this.snack(message.message),
        () => this.snack('Export failed')
      );
  }

  delete(data_source_id: number) {
    this.dataSourceService.deleteApiDataSourceId(data_source_id)
      .subscribe(
        (message) => {
          this.snack(message.message);
          const project = this.activeProject.project$.value;
          if (project === null) {
            return;
          }
          const newProject = {
            ...project,
            data_sources: project.data_sources.filter((data_source) => data_source.id !== data_source_id)
          };
          this.activeProject.project$.next(newProject);
        },
        () => this.snack('Failed to delete the resource')
      );
  }
}
