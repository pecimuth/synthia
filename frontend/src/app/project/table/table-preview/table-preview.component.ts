import { Component, OnInit, Input, OnDestroy } from '@angular/core';
import { TableView } from 'src/app/api/models/table-view';
import { TablePreviewView } from 'src/app/api/models/table-preview-view';
import { TableService } from 'src/app/api/services';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-table-preview',
  templateUrl: './table-preview.component.html',
  styleUrls: ['./table-preview.component.scss']
})
export class TablePreviewComponent implements OnInit, OnDestroy {

  private _table: TableView;
  get table(): TableView {
    return this._table;
  }
  @Input() set table(newTable: TableView) {
    this.unsubscribe();
    this._table = newTable;
    this.displayedColumns = this.table.columns.map((column) => column.name);
    this.previewSub = this.tableService.getApiTableIdPreview(this.table.id)
      .subscribe((preview) => this.preview = preview);
  }

  preview: TablePreviewView = {rows: []};
  displayedColumns: string[] = [];
  private previewSub: Subscription;

  constructor(
    private tableService: TableService
  ) { }

  ngOnInit(): void {}

  ngOnDestroy() {
    this.unsubscribe();
  }

  private unsubscribe() {
    if (this.previewSub) {
      this.previewSub.unsubscribe();
    }
  }
}
