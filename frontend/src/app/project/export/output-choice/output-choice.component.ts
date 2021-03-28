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

  /**
   * Output choice selection events.
   */
  @Output() outputChoiceChanged = new EventEmitter<DataSourceView | string | null>();

  /**
   * Available output file drivers.
   */
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

  /**
   * Trigger a new output choice selection event.
   * 
   * @param value - The value of the selection
   */
  choose(value: DataSourceView | string | null) {
    this.outputChoiceChanged.emit(value);
  }
}
