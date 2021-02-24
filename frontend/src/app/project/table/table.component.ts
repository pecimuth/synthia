import { Component, Input, OnInit } from '@angular/core';
import { TableView } from 'src/app/api/models/table-view';
import { ColumnView } from 'src/app/api/models/column-view';
import { MatDialog } from '@angular/material/dialog';
import { GeneratorChoiceComponent } from './generator-choice/generator-choice.component';

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss']
})
export class TableComponent implements OnInit {

  @Input() table: TableView;
  displayedColumns = ['column', 'generator', 'parameters', 'null_frequency'];

  constructor(
    private dialog: MatDialog,
  ) { }

  ngOnInit(): void {
  }

  chooseGenerator(column: ColumnView) {
    this.dialog.open(GeneratorChoiceComponent, {
      data: {
        column: column,
        table: this.table
      }
    });
  }
}
