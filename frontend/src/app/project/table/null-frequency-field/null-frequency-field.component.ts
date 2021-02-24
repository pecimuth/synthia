import { Component, Input, OnInit } from '@angular/core';
import { Subject, Subscription } from 'rxjs';
import { debounceTime, switchMap } from 'rxjs/operators';
import { ColumnView } from 'src/app/api/models/column-view';
import { TableView } from 'src/app/api/models/table-view';
import { GeneratorFacadeService } from '../../service/generator-facade.service';

@Component({
  selector: 'app-null-frequency-field',
  templateUrl: './null-frequency-field.component.html',
  styleUrls: ['./null-frequency-field.component.scss']
})
export class NullFrequencyFieldComponent implements OnInit {

  @Input() table: TableView;
  @Input() column: ColumnView;

  show = false;

  private genSub: Subscription;
  private fieldSub: Subscription;
  private valueChanges = new Subject<number>();

  constructor(
    private generatorFacade: GeneratorFacadeService
  ) { }

  ngOnInit(): void {
    this.genSub = this.generatorFacade.generators$
      .subscribe((generators) => {
        if (!this.column.generator_setting) {
          this.show = false;
        }
        const generator = generators.items
          .find((item) => item.name === this.column.generator_setting.name);
        this.show = generator.supports_null;
      });
    this.fieldSub = this.valueChanges
      .pipe(
        debounceTime(2000),
        switchMap(
          (value) => this.generatorFacade
            .patchParams(
              this.table.id,
              this.column.generator_setting,
              {null_frequency: value}
            )
        )
      )
      .subscribe();
  }

  ngOnDestroy() {
    this.unsubscribe();
    this.valueChanges.complete();
  }

  nextValue(value: string) {
    const parsed = parseFloat(value);
    if (!isNaN(parsed)) {
      this.valueChanges.next(parsed / 100);
    }
  }

  private unsubscribe() {
    if (this.genSub) {
      this.genSub.unsubscribe();
    }
    if (this.fieldSub) {
      this.fieldSub.unsubscribe();
    }
  }
}
