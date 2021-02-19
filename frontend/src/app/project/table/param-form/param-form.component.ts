import { Component, OnInit, Input, OnDestroy } from '@angular/core';
import { ColumnView } from 'src/app/api/models/column-view';
import { GeneratorFacadeService } from 'src/app/service/generator-facade.service';
import { FormGroup, FormBuilder } from '@angular/forms';
import { Subscription } from 'rxjs';
import { GeneratorListView } from 'src/app/api/models/generator-list-view';
import { switchMap, debounceTime } from 'rxjs/operators';
import { ColumnService } from 'src/app/api/services';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';

@Component({
  selector: 'app-param-form',
  templateUrl: './param-form.component.html',
  styleUrls: ['./param-form.component.scss']
})
export class ParamFormComponent implements OnInit, OnDestroy {

  private _column: ColumnView;
  
  get column(): ColumnView {
    return this._column;
  }

  @Input() set column(newColumn: ColumnView) {
    this._column = newColumn;
    if (!this.column.generator_name) {
      this.generator = undefined;
      this.form = undefined;
    }
    this.unsubscribe();
    this.genSub = this.generatorFacade.generators$
      .subscribe((generators) => this.createForm(generators));
    this.formSub = this.form.valueChanges
      .pipe(
        debounceTime(500),
        switchMap(
          (values) => this.columnService.patchApiColumnId(
            {
              id: this.column.id,
              column: {
                generator_name: this.column.generator_name,
                generator_params: values
              }
            }
          )
        )
      ).subscribe(
        (column) => this.projectFacade.refreshList() // TODO
      );
  }

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
    private columnService: ColumnService,
    private fb: FormBuilder,
    private projectFacade: ProjectFacadeService
  ) { }

  ngOnInit(): void {}

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
      .find((item) => item.name === this.column.generator_name);
    const options = {};
    this.generator.param_list.forEach((param) => {
      options[param.name] = [null];
    });
    if (this.column.generator_params) {
      Object.entries(this.column.generator_params)
        .forEach(([key, value]) => {
          if (options.hasOwnProperty(key)) {
            options[key] = [value];
          }
        });
    }
    this.form = this.fb.group(options);
  }

  getInputType(param: {name?: string, value_type?: string}): string {
    return (param.value_type === 'integer') ? 'number' : 'text';
  }
}
