import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { TableView } from 'src/app/api/models/table-view';
import { ColumnView } from 'src/app/api/models/column-view';
import { MatDialog } from '@angular/material/dialog';
import { GeneratorChoiceComponent } from './generator-choice/generator-choice.component';
import { Subject } from 'rxjs';
import { TableFacadeService } from '../service/table-facade.service';
import { takeUntil } from 'rxjs/operators';
import { ColumnFacadeService } from '../service/column-facade.service';
import { CreateColumnFormComponent } from './create-column-form/create-column-form.component';

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
    private columnFacade: ColumnFacadeService
  ) { }

  ngOnInit(): void {
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  chooseGenerator(column: ColumnView) {
    this.dialog.open(GeneratorChoiceComponent, {
      data: {
        columnId: column.id,
        tableId: this.table.id
      }
    });
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
      .subscribe();
  }

  deleteColumn(column: ColumnView) {
    this.columnFacade.deleteColumn(this.table.id, column.id)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe();
  }
}
