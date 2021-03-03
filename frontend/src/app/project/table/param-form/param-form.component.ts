import { Component, OnInit, Input, OnDestroy, Inject, LOCALE_ID } from '@angular/core';
import { ColumnView } from 'src/app/api/models/column-view';
import { GeneratorFacadeService, GeneratorParam, GeneratorView } from 'src/app/project/service/generator-facade.service';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { EMPTY, Observable, Subject } from 'rxjs';
import { switchMap, debounceTime, takeUntil, tap, filter } from 'rxjs/operators';
import { TableView } from 'src/app/api/models/table-view';
import { GeneratorSettingView } from 'src/app/api/models/generator-setting-view';
import { formatNumber } from '@angular/common';
import { SnackService } from 'src/app/service/snack.service';
import { DateAdapter, MatDateFormats, MAT_DATE_FORMATS, MAT_DATE_LOCALE } from '@angular/material/core';
import { MAT_MOMENT_DATE_ADAPTER_OPTIONS, MomentDateAdapter } from '@angular/material-moment-adapter';

const TYPE_DEBOUNCE_MS = 3000;

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
  
  @Input() table: TableView;
  @Input() column: ColumnView;

  form: FormGroup;
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
              formatted = formatNumber(value, this.localeId, '1.0-2');
            }
            options[key] = [formatted, Validators.required];
          }
        });
    }
    this.form = this.fb.group(options);
  }

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
                this.column.generator_setting,
                {params: params}
              );
          }
        )
      );
  }

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
