import { formatNumber } from '@angular/common';
import { Component, Inject, Input, LOCALE_ID, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MAT_MOMENT_DATE_ADAPTER_OPTIONS, MomentDateAdapter } from '@angular/material-moment-adapter';
import { DateAdapter, MatDateFormats, MAT_DATE_FORMATS, MAT_DATE_LOCALE } from '@angular/material/core';
import { EMPTY, Observable, Subject } from 'rxjs';
import { debounceTime, switchMap, takeUntil, tap } from 'rxjs/operators';
import { ColumnView } from 'src/app/api/models/column-view';
import { GeneratorSettingView } from 'src/app/api/models/generator-setting-view';
import { TableView } from 'src/app/api/models/table-view';
import { GeneratorFacadeService, GeneratorParam, GeneratorView } from 'src/app/project/service/generator-facade.service';
import { SnackService } from 'src/app/service/snack.service';

/**
 * Patch the generator settings when at least TYPE_DEBOUNCE_MS ms
 * elapsed after the last value change.
 */
const TYPE_DEBOUNCE_MS = 3000;

/**
 * Settings for the date input element. 
 */
export const DATE_FORMATS: MatDateFormats = {
  parse: {
    dateInput: 'YYYY-MM-DD',
  },
  display: {
    dateInput: 'YYYY-MM-DD',
    monthYearLabel: 'MMM YYYY',
    dateA11yLabel: 'LL',
    monthYearA11yLabel: 'MMMM YYYY',
  }
};

@Component({
  selector: 'app-param-form',
  templateUrl: './param-form.component.html',
  styleUrls: ['./param-form.component.scss'],
  providers: [
    {
      provide: DateAdapter,
      useClass: MomentDateAdapter,
      deps: [MAT_DATE_LOCALE, MAT_MOMENT_DATE_ADAPTER_OPTIONS]
    },
    {provide: MAT_DATE_FORMATS, useValue: DATE_FORMATS},
  ],
})
export class ParamFormComponent implements OnInit, OnDestroy {
  
  /**
   * Table containing the column.
   */
  @Input() table: TableView;

  /**
   * The column for whose generator we are responsible.
   */
  @Input() column: ColumnView;

  /**
   * Parameter form with a structure dependent on the assigned generator.
   */
  form: FormGroup;

  /**
   * The generator type fetched by the input column generator name.
   */
  generator: GeneratorView;

  private unsubscribe$ = new Subject();

  constructor(
    private generatorFacade: GeneratorFacadeService,
    private fb: FormBuilder,
    private snackService: SnackService,
    @Inject(LOCALE_ID) public localeId: string
  ) { }

  ngOnInit(): void {
    const generatorName = this.column?.generator_setting?.name;
    if (!generatorName) {
      return;
    }
    this.generatorFacade.getGeneratorByName(generatorName)
      .pipe(
        takeUntil(this.unsubscribe$),
        tap((generator) => {
          this.generator = generator;
          this.createForm();
        }),
        switchMap(() => this.handleFormChanges())
      )
      .subscribe(
        () => null,
        (err) => this.snackService.errorIntoSnack(err, 'Failed to update parameters')
      );
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  /**
   * Create the form based on the generator parameter definitions.
   */
  private createForm() {
    if (!this.generator) {
      this.form = undefined;
      return;
    }
    const options = {};
    this.generator.param_list.forEach((param) => {
      options[param.name] = [null];
    });
    if (this.column?.generator_setting?.params) {
      Object.entries(this.column.generator_setting.params)
        .forEach(([key, value]) => {
          if (options.hasOwnProperty(key)) {
            let formatted = value;
            if (typeof value === 'number') {
              formatted = formatNumber(value, this.localeId, '1.0-2').replace(/,/g, '');
            }
            options[key] = [formatted, Validators.required];
          }
        });
    }
    this.form = this.fb.group(options);
  }

  /**
   * Observe form value changes and patch the generator setting parameters.
   * 
   * @returns Observable of the patched setting.
   */
  private handleFormChanges(): Observable<GeneratorSettingView> {
    return this.form.valueChanges
      .pipe(
        debounceTime(TYPE_DEBOUNCE_MS),
        switchMap(
          (params) => {
            if (!this.form.valid) {
              return EMPTY;
            }
            return this.generatorFacade
              .patchParams(
                this.table.id,
                this.column.generator_setting.id,
                {params: params}
              );
          }
        )
      );
  }

  /**
   * Convert a generator parameter to input type.
   * Returns `select` for a select element, `number` and `text` to be used as HTML input
   * types and `datetime` for a date input element.
   * 
   * @param param - Generator parameter definition
   * @returns Form input type
   */
  getInputType(param: GeneratorParam): string {
    if (param.allowed_values) {
      return 'select';
    }
    if (param.value_type === 'integer' || param.value_type == 'float') {
      return 'number';
    }
    if (param.value_type === 'datetime') {
      return 'datetime';
    }
    return 'text';
  }
}
