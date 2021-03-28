import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { DataSourceView } from 'src/app/api/models/data-source-view';
import { DatabaseSourceFormComponent } from 'src/app/dialog/database-source-form/database-source-form.component';
import { SnackService } from 'src/app/service/snack.service';
import { DataSourceFacadeService } from '../service/data-source-facade.service';

@Component({
  selector: 'app-resource',
  templateUrl: './resource.component.html',
  styleUrls: ['./resource.component.scss']
})
export class ResourceComponent implements OnInit, OnDestroy {

  /**
   * The data source we are responsible for.
   */
  @Input() dataSource: DataSourceView;

  /**
   * Should a progress bar be visible?
   */
  showProgress = false;

  private unsubscribe$ = new Subject();
  
  constructor(
    private dataSourceFacade: DataSourceFacadeService,
    private snackService: SnackService,
    private dialog: MatDialog
  ) { }

  ngOnInit(): void {
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  /**
   * Import schema from the data source.
   */
  import() {
    this.showProgress = true;
    this.dataSourceFacade.import(this.dataSource.id)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(
        () => {
          this.snackService.snack('Successfully imported the schema');
          this.showProgress = false;
        },
        (err) => {
          this.snackService.errorIntoSnack(err, 'Failed to import the schema');
          this.showProgress = false;
        }
      );
  }

  /**
   * Delete the data source via the API.
   */
  delete() {
    this.dataSourceFacade.delete(this.dataSource.id)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(
        () => null,
        (err) => this.snackService.errorIntoSnack(err, 'Failed to deleted the resource')
      );
  }

  /**
   * Download the data source file.
   */
  download() {
    this.dataSourceFacade.download(this.dataSource.id)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(
        () => null,
        (err) => this.snackService.errorIntoSnack(err, 'Failed to download the file')
      );
  }

  /**
   * Open the edit database resource dialog.
   */
  editDatabase() {
    this.dialog.open(DatabaseSourceFormComponent, {data: this.dataSource});
  }
}
