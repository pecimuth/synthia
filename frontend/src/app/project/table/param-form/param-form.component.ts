import { Component, OnInit, Input, OnDestroy } from '@angular/core';
import { ColumnView } from 'src/app/api/models/column-view';
import { GeneratorFacadeService } from 'src/app/project/service/generator-facade.service';
import { FormGroup, FormBuilder } from '@angular/forms';
import { Subscription } from 'rxjs';
import { GeneratorListView } from 'src/app/api/models/generator-list-view';
import { switchMap, debounceTime } from 'rxjs/operators';
import { TableView } from 'src/app/api/models/table-view';

@Component({
  selector: 'app-param-form',
  templateUrl: './param-form.component.html',
  styleUrls: ['./param-form.component.scss']
})
export class ParamFormComponent implements OnInit, OnDestroy {
  
  @Input() table: TableView;
  @Input() column: ColumnView;

  form: FormGroup;
  generator: {
    name?: string;
    param_list?: {
      name?: string;
      value_type?: string;
    }[];
  };
  private genSub: Subscription;
  private formSub: Subscription;

  constructor(
    private generatorFacade: GeneratorFacadeService,
    private fb: FormBuilder
  ) { }

  ngOnInit(): void {
    this.genSub = this.generatorFacade.generators$
      .subscribe((generators) => {
        this.createForm(generators)
        this.subscribeFormChanges();
      });
  }

  ngOnDestroy() {
    this.unsubscribe();
  }

  private unsubscribe() {
    if (this.genSub) {
      this.genSub.unsubscribe();
    }
    if (this.formSub) {
      this.formSub.unsubscribe();
    }
  }

  private createForm(generators: GeneratorListView) {
    this.generator = generators.items
      .find((item) => item.name === this.column.generator_setting.name);
    const options = {};
    this.generator.param_list.forEach((param) => {
      options[param.name] = [null];
    });
    if (this.column.generator_setting.params) {
      Object.entries(this.column.generator_setting.params)
        .forEach(([key, value]) => {
          if (options.hasOwnProperty(key)) {
            options[key] = [value];
          }
        });
    }
    this.form = this.fb.group(options);
  }

  private subscribeFormChanges() {
    if (this.formSub) {
      this.formSub.unsubscribe();
    }
    this.formSub = this.form.valueChanges
      .pipe(
        debounceTime(500),
        switchMap(
          (params) => this.generatorFacade
            .patchParams(
              this.table.id,
              this.column.generator_setting,
              {params: params}
            )
        )
      )
      .subscribe();
  }

  getInputType(param: {name?: string, value_type?: string}): string {
    return (param.value_type === 'integer') ? 'number' : 'text';
  }
}
