import { Component, Input, OnInit } from '@angular/core';
import { TableView } from 'src/app/api/models/table-view';

type TablePreview = Array<{[key: string]: any}>

@Component({
  selector: 'app-table-preview',
  templateUrl: './table-preview.component.html',
  styleUrls: ['./table-preview.component.scss']
})
export class TablePreviewComponent implements OnInit {

  /**
   * The table for whose preview we are responsible.
   */
  private _table: TableView;

  get table(): TableView {
    return this._table;
  }

  /**
   * Set the table. List of displayed columns is constructed from the list
   * of assigned table columns.
   */
  @Input() set table(newTable: TableView) {
    this._table = newTable;
    this.displayedColumns = this.table.columns.map((column) => column.name);
  }

  /**
   * Generated preview for our table.
   */
  @Input() preview: TablePreview;

  /**
   * The list of column names displayed in the grid.
   */
  displayedColumns: string[] = [];

  constructor() { }

  ngOnInit(): void {
  }
}
