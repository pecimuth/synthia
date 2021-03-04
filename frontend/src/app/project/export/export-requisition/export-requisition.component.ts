import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { MatCheckboxChange } from '@angular/material/checkbox';
import { ExportRequisitionView } from 'src/app/api/models/export-requisition-view';
import { ProjectView } from 'src/app/api/models/project-view';

const BASE_COUNT = 10;

interface Inclusion {
  included: boolean;
}

type RequisitionRows = ExportRequisitionView['rows'];
type RequisitionRow = RequisitionRows[0];

@Component({
  selector: 'app-export-requisition',
  templateUrl: './export-requisition.component.html',
  styleUrls: ['./export-requisition.component.scss']
})
export class ExportRequisitionComponent implements OnInit {

  requisitionRows: Array<RequisitionRow & Inclusion>;
  allIncluded = true;
  indeterminate = false;

  private _project: ProjectView;
  @Input() set project(newProject: ProjectView) {
    this._project = newProject;
    this.allIncluded = true;
    this.indeterminate = false;
    this.requisitionRows = newProject.tables
      .map((table, index) => {
        return {
          table_name: table.name,
          row_count: BASE_COUNT,
          seed: index,
          included: true,
        };
      });
    this.emit();
  }
  get project(): ProjectView {
    return this._project;
  }

  @Output() requisitionChanged = new EventEmitter<ExportRequisitionView>();

  displayedColumns = ['table', 'row_count', 'seed'];

  constructor() { }

  ngOnInit(): void {}

  include(row: RequisitionRow & Inclusion, event: MatCheckboxChange) {
    row.included = event.checked;
    this.allIncluded = row.included && this.requisitionRows.every((other) => other.included);
    this.indeterminate = !this.allIncluded && this.requisitionRows.some((other) => other.included);
    this.emit();
  }

  includeAll(event: MatCheckboxChange) {
    this.allIncluded = event.checked;
    this.requisitionRows.forEach((row) => row.included = event.checked);
    this.indeterminate = false;
    this.emit();
  }

  changeRowCount(row: RequisitionRow & Inclusion, newCount: string) {
    row.row_count = parseInt(newCount) || 0;
    this.emit();
  }

  changeSeed(row: RequisitionRow & Inclusion, newSeed: string) {
    row.seed = parseInt(newSeed) || 0;
    this.emit();
  }

  private emit() {
    const result: ExportRequisitionView = {
      rows: []
    };
    this.requisitionRows
      .filter((row) => row.included)
      .forEach(
        (item) => result.rows.push({
          table_name: item.table_name,
          row_count: item.row_count,
          seed: item.seed
        })
      );
    this. requisitionChanged.emit(result);
  }
}
