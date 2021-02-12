import { Component, OnInit, Input } from '@angular/core';
import { TableView } from 'src/app/api/models/table-view';

type TablePreview = Array<{[key: string]: any}>

@Component({
  selector: 'app-table-preview',
  templateUrl: './table-preview.component.html',
  styleUrls: ['./table-preview.component.scss']
})
export class TablePreviewComponent implements OnInit {

  private _table: TableView;
  get table(): TableView {
    return this._table;
  }
  @Input() set table(newTable: TableView) {
    this._table = newTable;
    this.displayedColumns = this.table.columns.map((column) => column.name);
  }

  @Input() preview: TablePreview;

  displayedColumns: string[] = [];

  constructor() { }

  ngOnInit(): void {
  }
}
