import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { DataSourceView } from 'src/app/api/models/data-source-view';
import { ProjectView } from 'src/app/api/models/project-view';

@Component({
  selector: 'app-output-choice',
  templateUrl: './output-choice.component.html',
  styleUrls: ['./output-choice.component.scss']
})
export class OutputChoiceComponent implements OnInit {

  @Input() project: ProjectView;
  @Output() outputChoiceChanged = new EventEmitter<DataSourceView | string>();

  constructor() { }

  ngOnInit(): void {
  }

  onChange(value: DataSourceView | string) {
    this.outputChoiceChanged.emit(value);
  }
}
