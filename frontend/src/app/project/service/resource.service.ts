import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DataSourceService } from 'src/app/api/services';
import { ActiveProjectService } from './active-project.service';
import { Snack } from 'src/app/service/constants';
import { DataSourceDatabaseWrite } from 'src/app/api/models/data-source-database-write';

@Injectable({
  providedIn: 'root'
})
export class ResourceService {

  constructor(
    private activeProject: ActiveProjectService,
    private snackBar: MatSnackBar,
    private dataSourceService: DataSourceService
  ) { }

  private snack(message: string) {
    this.snackBar.open(message, Snack.OK, Snack.CONFIG);
  }

  import(dataSourceId: number) {
    this.dataSourceService.postApiDataSourceIdImport(dataSourceId)
      .subscribe(
        (project) => {
          this.snack('Successfully imported the schema')
          this.activeProject.project$.next(project);
        },
        () => this.snack('Import failed')
      );
  }

  delete(dataSourceId: number) {
    this.dataSourceService.deleteApiDataSourceId(dataSourceId)
      .subscribe(
        (message) => {
          this.snack(message.message);
          this.activeProject.deleteDataSource(dataSourceId);
        },
        () => this.snack('Failed to delete the resource')
      );
  }

  createDatabase(dataSourceDatabase: DataSourceDatabaseWrite) {
    const project = this.activeProject.project$.value;
    dataSourceDatabase.project_id = project.id;

    this.dataSourceService.postApiDataSourceDatabase(dataSourceDatabase)
      .subscribe(
        (dataSource) => {
          this.snack('Database added');  
          this.activeProject.addDataSource(dataSource);
        },
        () => this.snack('Failed to create a database resource')
      );
  }

  createFileSource(dataFile: Blob) {
    const project = this.activeProject.project$.value;
    const params = {
      projectId: project.id,
      dataFile: dataFile
    }

    this.dataSourceService.postApiDataSourceFile(params)
      .subscribe(
        (dataSource) => {
          this.snack('File uploaded');     
          this.activeProject.addDataSource(dataSource);
        },
        () => this.snack('Failed to create a file resource')
      );
  }

  mockDatabase() {
    const project = this.activeProject.project$.value;
    this.dataSourceService.postApiDataSourceMockDatabase(project.id)
      .subscribe(
        (dataSource) => {
          this.snack('Database created');     
          this.activeProject.addDataSource(dataSource);
        },
        () => this.snack('Failed to create a mock database')
      );
  }
}
