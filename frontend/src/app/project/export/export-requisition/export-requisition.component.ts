import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { MatCheckboxChange } from '@angular/material/checkbox';
import { ExportRequisitionView } from 'src/app/api/models/export-requisition-view';
import { ProjectView } from 'src/app/api/models/project-view';

const BASE_COUNT = 10;

interface InclusionValidity {
  included: boolean;
  rowCountValid: boolean;
  seedValid: boolean;
}

type RequisitionRows = ExportRequisitionView['rows'];
type RequisitionRow = RequisitionRows[0];

@Component({
  selector: 'app-export-requisition',
  templateUrl: './export-requisition.component.html',
  styleUrls: ['./export-requisition.component.scss']
})
export class ExportRequisitionComponent implements OnInit {

  requisitionRows: Array<RequisitionRow & InclusionValidity>;
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
          rowCountValid: true,
          seedValid: true
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

  include(row: RequisitionRow & InclusionValidity, event: MatCheckboxChange) {
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

  changeRowCount(row: RequisitionRow & InclusionValidity, newCount: string) {
    const parsed = parseInt(newCount);
    row.rowCountValid = parsed > 0;
    if (parsed > 0) {
      row.row_count = parsed;
      this.emit();
    } else {
      this.requisitionChanged.emit();
    }
  }

  changeSeed(row: RequisitionRow & InclusionValidity, newSeed: string) {
    const parsed = parseInt(newSeed);
    row.seedValid = !isNaN(parsed);
    if (!isNaN(parsed)) {
      row.seed = parsed;
      this.emit();
    } else {
      this.requisitionChanged.emit();
    }
  }

  private emit() {
    const result: ExportRequisitionView = {
      rows: []
    };
    let valid = true;
    this.requisitionRows
      .filter((row) => row.included)
      .forEach(
        (row) => {
          result.rows.push({
            table_name: row.table_name,
            row_count: row.row_count,
            seed: row.seed
          });
          if (!row.seedValid || !row.rowCountValid) {
            valid = false;
          }
        }
      );

    if (valid) {
      this.requisitionChanged.emit(result);
    } else {
      this.requisitionChanged.emit();
    }
  }
}
