import { Component, OnInit, Input } from '@angular/core';
import { MatSelectChange } from '@angular/material/select';
import { ColumnView } from 'src/app/api/models/column-view';
import { Observable } from 'rxjs';
import { GeneratorListView } from 'src/app/api/models/generator-list-view';
import { GeneratorFacadeService } from 'src/app/service/generator-facade.service';
import { ColumnService } from 'src/app/api/services';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';

@Component({
  selector: 'app-generator-select',
  templateUrl: './generator-select.component.html',
  styleUrls: ['./generator-select.component.scss']
})
export class GeneratorSelectComponent implements OnInit {

  @Input() column: ColumnView;
  generators$: Observable<GeneratorListView>;

  constructor(
    private generatorFacade: GeneratorFacadeService,
    private columnService: ColumnService,
    private projectFacade: ProjectFacadeService
  ) { }

  ngOnInit(): void {
    this.generators$ = this.generatorFacade.generators$;
  }

  onSelectionChange(event: MatSelectChange) {
    this.columnService.patchApiColumnId({
      id: this.column.id,
      column: {
        generator_params: {},
        generator_name: event.value
      }
    }).subscribe((column) => this.projectFacade.refreshList()); // TODO
  }
}
