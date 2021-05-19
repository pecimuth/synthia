import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { GeneratorSettingView } from 'src/app/api/models';
import { ColumnView } from 'src/app/api/models/column-view';
import { TableView } from 'src/app/api/models/table-view';
import { GeneratorFacadeService, GeneratorView } from '../../service/generator-facade.service';
import { GeneratorChoiceComponent } from '../generator-choice/generator-choice.component';

@Component({
  selector: 'app-generator-field',
  templateUrl: './generator-field.component.html',
  styleUrls: ['./generator-field.component.scss']
})
export class GeneratorFieldComponent implements OnInit, OnDestroy {

  /**
   * Table containing the column.
   */
  @Input() table: TableView;

  /**
   * The column for whose generator we are responsible.
   */
  @Input() column: ColumnView;

  /**
   * Generator setting of the column.
   */
  setting: GeneratorSettingView;

  /**
   * The generator type fetched by the input column generator name.
   */
   generator: GeneratorView;

   private unsubscribe$ = new Subject();

  constructor(
    private dialog: MatDialog,
    public generatorFacade: GeneratorFacadeService
  ) { }

  ngOnInit(): void {
    this.setting = this.column?.generator_setting;
    if (!this.setting) {
      return;
    }
    this.generatorFacade.getGeneratorByName(this.setting.name)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe((generator) => this.generator = generator);
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  chooseGenerator() {
    this.dialog.open(GeneratorChoiceComponent, {
      data: {
        columnId: this.column.id,
        tableId: this.table.id
      }
    });
  }
}
