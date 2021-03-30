import { Component, Input, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { debounceTime, switchMap, takeUntil } from 'rxjs/operators';
import { ColumnView } from 'src/app/api/models/column-view';
import { TableView } from 'src/app/api/models/table-view';
import { SnackService } from 'src/app/service/snack.service';
import { GeneratorFacadeService } from '../../service/generator-facade.service';

/**
 * Patch the null frequency parameter when at least TYPE_DEBOUNCE_MS ms
 * elapsed after the last value change.
 */
const TYPE_DEBOUNCE_MS = 2000;

@Component({
  selector: 'app-null-frequency-field',
  templateUrl: './null-frequency-field.component.html',
  styleUrls: ['./null-frequency-field.component.scss']
})
export class NullFrequencyFieldComponent implements OnInit {

  /**
   * Table containing the column.
   */
  @Input() table: TableView;

  /**
   * The column for whose null frequency parameter we are responsible.
   */
  @Input() column: ColumnView;

  /**
   * Should the input be shown?
   */
  show = false;

  private unsubscribe$ = new Subject();

  /**
   * Subject of null frequency changes.
   */
  private valueChanges$ = new Subject<number>();

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
        this.show = !!generator?.supports_null &&
          (generator.is_multi_column || this.column?.nullable);
      });

    this.valueChanges$
      .pipe(
        debounceTime(TYPE_DEBOUNCE_MS),
        switchMap(
          (value) => this.generatorFacade
            .patchParams(
              this.table.id,
              this.column.generator_setting.id,
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
    this.valueChanges$.complete();
  }

  /**
   * Handle a null frequency change by the user.
   * 
   * @param value - The user input value
   */
  nextValue(value: string) {
    const parsed = parseFloat(value);
    if (!isNaN(parsed)) {
      this.valueChanges$.next(this.fromPercent(parsed));
    }
  }

  /**
   * Convert the null frequency to percent value.
   * 
   * @param value - The value from interval [0;1]
   * @returns Value from interval [0;100]
   */
  toPercent(value: number): number {
    return value * 100;
  }

  /**
   * Convert a percent value to null frequency.
   * 
   * @param value - The value from interval [0;100]
   * @returns Value from interval [0;1]
   */
  fromPercent(value: number): number {
    return value / 100;
  }
}
