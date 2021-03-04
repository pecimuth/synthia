import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { DataSourceView } from 'src/app/api/models/data-source-view';
import { OutputFileDriverListView } from 'src/app/api/models/output-file-driver-list-view';
import { ProjectView } from 'src/app/api/models/project-view';
import { GeneratorService } from 'src/app/api/services';

@Component({
  selector: 'app-output-choice',
  templateUrl: './output-choice.component.html',
  styleUrls: ['./output-choice.component.scss']
})
export class OutputChoiceComponent implements OnInit {

  @Input() project: ProjectView;
  @Output() outputChoiceChanged = new EventEmitter<DataSourceView | string>();

  fileDrivers: OutputFileDriverListView = {items: []};
  private unsubscribe$ = new Subject();

  constructor(private generatorService: GeneratorService) { }

  ngOnInit(): void {
    this.generatorService.getApiOutputFileDrivers()
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe((drivers) => this.fileDrivers = drivers);
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  onChange(value: DataSourceView | string) {
    this.outputChoiceChanged.emit(value);
  }
}
