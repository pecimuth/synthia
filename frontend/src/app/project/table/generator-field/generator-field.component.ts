import { Component, Input, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ColumnView } from 'src/app/api/models/column-view';
import { TableView } from 'src/app/api/models/table-view';
import { GeneratorFacadeService } from '../../service/generator-facade.service';
import { GeneratorChoiceComponent } from '../generator-choice/generator-choice.component';

@Component({
  selector: 'app-generator-field',
  templateUrl: './generator-field.component.html',
  styleUrls: ['./generator-field.component.scss']
})
export class GeneratorFieldComponent implements OnInit {

  @Input() table: TableView;
  @Input() column: ColumnView;

  constructor(
    private dialog: MatDialog,
    public generatorFacade: GeneratorFacadeService
  ) { }

  ngOnInit(): void {
  }

  chooseGenerator(column: ColumnView) {
    this.dialog.open(GeneratorChoiceComponent, {
      data: {
        columnId: column.id,
        tableId: this.table.id
      }
    });
  }
}
