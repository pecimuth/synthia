import { Component, OnInit, Input, OnDestroy, Inject, LOCALE_ID } from '@angular/core';
import { ColumnView } from 'src/app/api/models/column-view';
import { GeneratorFacadeService, GeneratorParam, GeneratorView } from 'src/app/project/service/generator-facade.service';
import { FormGroup, FormBuilder } from '@angular/forms';
import { Observable, Subject } from 'rxjs';
import { switchMap, debounceTime, takeUntil, tap } from 'rxjs/operators';
import { TableView } from 'src/app/api/models/table-view';
import { GeneratorSettingView } from 'src/app/api/models/generator-setting-view';
import { formatNumber } from '@angular/common';

const TYPE_DEBOUNCE_MS = 3000;

@Component({
  selector: 'app-param-form',
  templateUrl: './param-form.component.html',
  styleUrls: ['./param-form.component.scss']
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
      .subscribe();
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
            options[key] = [formatted];
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
          (params) => this.generatorFacade
            .patchParams(
              this.table.id,
              this.column.generator_setting,
              {params: params}
            )
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
