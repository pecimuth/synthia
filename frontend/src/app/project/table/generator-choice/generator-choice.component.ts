import { Component, Inject, OnDestroy, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Subject } from 'rxjs';
import { switchMap, takeUntil, tap } from 'rxjs/operators';
import { ColumnView } from 'src/app/api/models/column-view';
import { GeneratorSettingView } from 'src/app/api/models/generator-setting-view';
import { TableView } from 'src/app/api/models/table-view';
import { GeneratorFacadeService, GeneratorView } from 'src/app/project/service/generator-facade.service';
import { ActiveProjectService } from '../../service/active-project.service';
import { ColumnFacadeService } from '../../service/column-facade.service';

export interface GeneratorChoiceInput {
  columnId: number,
  tableId: number
}

@Component({
  selector: 'app-generator-choice',
  templateUrl: './generator-choice.component.html',
  styleUrls: ['./generator-choice.component.scss']
})
export class GeneratorChoiceComponent implements OnInit, OnDestroy {

  column: ColumnView;
  table: TableView;
  generators: GeneratorView[];
  private unsubscribe$ = new Subject();

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: GeneratorChoiceInput,
    private dialogRef: MatDialogRef<GeneratorChoiceComponent>,
    private generatorFacade: GeneratorFacadeService,
    private columnFacade: ColumnFacadeService,
    private activeProject: ActiveProjectService
  ) { }

  ngOnInit(): void {
    this.activeProject.getTableColumn(this.data.tableId, this.data.columnId)
      .pipe(
        takeUntil(this.unsubscribe$),
        tap(([table, column]) => {
          this.table = table;
          this.column = column;
        }),
        switchMap(([table, column]) => {
          return this.generatorFacade.getGeneratorsForColumn(column);
        })
      )
      .subscribe(
        (generators) => this.generators = generators
      );
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  selectSetting(setting: GeneratorSettingView) {
    this.columnFacade
      .setColumnGeneratorSetting(
        this.table.id,
        this.column,
        setting
      )
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(() => this.dialogRef.close());
  }

  deleteSetting(setting: GeneratorSettingView) {
    this.generatorFacade
      .deleteSetting(
        this.table.id,
        setting
      )
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe();
  }

  createSetting(generator: GeneratorView) {
    this.generatorFacade
      .createSetting(
        this.table.id,
        this.column.id,
        generator
      )
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe();
  }
}
