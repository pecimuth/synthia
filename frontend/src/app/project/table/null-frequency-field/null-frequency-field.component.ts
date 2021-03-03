import { Component, Input, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { debounceTime, switchMap, takeUntil } from 'rxjs/operators';
import { ColumnView } from 'src/app/api/models/column-view';
import { TableView } from 'src/app/api/models/table-view';
import { SnackService } from 'src/app/service/snack.service';
import { GeneratorFacadeService } from '../../service/generator-facade.service';

const TYPE_DEBOUNCE_MS = 2000;

@Component({
  selector: 'app-null-frequency-field',
  templateUrl: './null-frequency-field.component.html',
  styleUrls: ['./null-frequency-field.component.scss']
})
export class NullFrequencyFieldComponent implements OnInit {

  @Input() table: TableView;
  @Input() column: ColumnView;

  show = false;

  private unsubscribe$ = new Subject();
  private valueChanges = new Subject<number>();

  constructor(
    private generatorFacade: GeneratorFacadeService,
    private snackService: SnackService
  ) { }

  ngOnInit(): void {
    const generatorName = this.column?.generator_setting?.name;
    if (!generatorName) {
      return;
    }

    this.generatorFacade.getGeneratorByName(generatorName)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe((generator) => {
        this.show = !!generator?.supports_null;
      });
    
    this.valueChanges
      .pipe(
        debounceTime(TYPE_DEBOUNCE_MS),
        switchMap(
          (value) => this.generatorFacade
            .patchParams(
              this.table.id,
              this.column.generator_setting,
              {null_frequency: value}
            )
        )
      )
      .subscribe(
        () => null,
        (err) => this.snackService.errorIntoSnack(err)
      );
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
    this.valueChanges.complete();
  }

  nextValue(value: string) {
    const parsed = parseFloat(value);
    if (!isNaN(parsed)) {
      this.valueChanges.next(this.fromPercent(parsed));
    }
  }

  toPercent(value: number): number {
    return value * 100;
  }

  fromPercent(value: number): number {
    return value / 100;
  }
}
