import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ColumnView } from 'src/app/api/models/column-view';
import { TableView } from 'src/app/api/models/table-view';
import { SnackService } from 'src/app/service/snack.service';
import { ColumnFacadeService } from '../service/column-facade.service';
import { TableFacadeService } from '../service/table-facade.service';
import { CreateColumnFormComponent } from './create-column-form/create-column-form.component';

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss']
})
export class TableComponent implements OnInit, OnDestroy {

  @Input() table: TableView;

  /**
   * Names of columns displayed in the grid.
   */
  displayedColumns = ['column', 'generator', 'parameters', 'null_frequency'];

  private unsubscribe$ = new Subject();

  constructor(
    private dialog: MatDialog,
    private tableFacade: TableFacadeService,
    private columnFacade: ColumnFacadeService,
    private snackService: SnackService
  ) { }

  ngOnInit(): void {
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  /**
   * Open the create column dialog for our table.
   */
  createColumn() {
    this.dialog.open(CreateColumnFormComponent, {
      data: {
        tableId: this.table.id
      }
    });
  }

  /**
   * Delete the table via the API.
   */
  deleteTable() {
    this.tableFacade.deleteTable(this.table.id)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(
        () => null,
        (err) => this.snackService.errorIntoSnack(err)
      );
  }

  /**
   * Delete a column via the API.
   * 
   * @param column - The column to be deleted
   */
  deleteColumn(column: ColumnView) {
    this.columnFacade.deleteColumn(column.id)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(
        () => null,
        (err) => this.snackService.errorIntoSnack(err)
      );
  }
}
