import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { TableView } from 'src/app/api/models/table-view';
import { ColumnView } from 'src/app/api/models/column-view';
import { MatDialog } from '@angular/material/dialog';
import { Subject } from 'rxjs';
import { TableFacadeService } from '../service/table-facade.service';
import { takeUntil } from 'rxjs/operators';
import { ColumnFacadeService } from '../service/column-facade.service';
import { CreateColumnFormComponent } from './create-column-form/create-column-form.component';
import { SnackService } from 'src/app/service/snack.service';

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss']
})
export class TableComponent implements OnInit, OnDestroy {

  @Input() table: TableView;
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

  createColumn() {
    this.dialog.open(CreateColumnFormComponent, {
      data: {
        tableId: this.table.id
      }
    });
  }

  deleteTable() {
    this.tableFacade.deleteTable(this.table.id)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(
        () => null,
        (err) => this.snackService.errorIntoSnack(err)
      );
  }

  deleteColumn(column: ColumnView) {
    this.columnFacade.deleteColumn(this.table.id, column.id)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(
        () => null,
        (err) => this.snackService.errorIntoSnack(err)
      );
  }
}
