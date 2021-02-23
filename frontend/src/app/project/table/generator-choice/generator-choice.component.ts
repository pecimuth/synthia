import { Component, Inject, OnDestroy, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Subscription } from 'rxjs';
import { ColumnView } from 'src/app/api/models/column-view';
import { GeneratorListView } from 'src/app/api/models/generator-list-view';
import { GeneratorSettingView } from 'src/app/api/models/generator-setting-view';
import { TableView } from 'src/app/api/models/table-view';
import { GeneratorFacadeService } from 'src/app/project/service/generator-facade.service';
import { ColumnFacadeService } from '../../service/column-facade.service';


export interface GeneratorChoiceInput {
  column: ColumnView,
  table: TableView
}

@Component({
  selector: 'app-generator-choice',
  templateUrl: './generator-choice.component.html',
  styleUrls: ['./generator-choice.component.scss']
})
export class GeneratorChoiceComponent implements OnInit, OnDestroy {

  generators: GeneratorListView;
  private generatorSubscription: Subscription;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: GeneratorChoiceInput,
    private dialogRef: MatDialogRef<GeneratorChoiceComponent>,
    private generatorFacade: GeneratorFacadeService,
    private columnFacade: ColumnFacadeService
  ) { }

  ngOnInit(): void {
    this.generatorSubscription = this.generatorFacade.generators$
      .subscribe(
        (generators) => this.filterGenerators(generators)
      );
  }

  ngOnDestroy() {
    this.unsubscribe();
  }

  selectSetting(setting: GeneratorSettingView) {
    this.columnFacade.setColumnGeneratorSetting(
      this.data.table,
      this.data.column,
      setting
    ).subscribe(() => this.dialogRef.close());
  }

  private unsubscribe() {
    if (this.generatorSubscription) {
      this.generatorSubscription.unsubscribe();
    }
  }

  private filterGenerators(generators: GeneratorListView) {
    const filteredItems = generators.items.filter(
      (generator) => {
        if (!this.data.column?.col_type || !generator.only_for_type) {
          return true;
        }
        return this.data.column.col_type === generator.only_for_type;
      }
    );
    this.generators = {
      items: filteredItems
    };
  }
}
