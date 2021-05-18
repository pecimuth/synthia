import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { ExportRequisitionView } from 'src/app/api/models/export-requisition-view';
import { ProjectView } from 'src/app/api/models/project-view';

/**
 * Default row count for each project table.
 */
const BASE_COUNT = 10;

/**
 * Row inclusion and input value validity.
 */
interface InclusionValidity {
  included: boolean;
  rowCountValid: boolean;
  seedValid: boolean;
}

type RequisitionRows = ExportRequisitionView['rows'];
type RequisitionRow = RequisitionRows[0];

type RowInclusionValidity = RequisitionRow & InclusionValidity;

@Component({
  selector: 'app-export-requisition',
  templateUrl: './export-requisition.component.html',
  styleUrls: ['./export-requisition.component.scss']
})
export class ExportRequisitionComponent implements OnInit {

  /**
   * Array of requisiton rows with their inclusions and input value validities.
   */
  requisitionRows: Array<RowInclusionValidity>;

  /**
   * Are all project tables included?
   */
  allIncluded = true;

  /**
   * Are there some tables included and some tables not included?
   */
  indeterminate = false;

  /**
   * The project we are reponsible for.
   */
  private _project: ProjectView;

  /**
   * Set the project. Update the component properties.
   */
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

  /**
   * Event triggered when the export requisition changes.
   */
  @Output() requisitionChanged = new EventEmitter<ExportRequisitionView>();

  /**
   * List of columns displayed in the grid.
   */
  displayedColumns = ['table', 'row_count', 'seed'];

  constructor() { }

  ngOnInit(): void {}

  /**
   * Set the requisition row's inclusion value.
   * 
   * @param row - The requisition row
   * @param included - The inclusion value
   */
  include(row: RowInclusionValidity, included: boolean) {
    row.included = included;
    this.allIncluded = row.included && this.requisitionRows.every((other) => other.included);
    this.indeterminate = !this.allIncluded && this.requisitionRows.some((other) => other.included);
    this.emit();
  }

  /**
   * Include or exclude all rows (tables).
   * 
   * @param included - The inclusion value for all rows
   */
  includeAll(included: boolean) {
    this.allIncluded = included
    this.requisitionRows.forEach((row) => row.included = included);
    this.indeterminate = false;
    this.emit();
  }

  /**
   * Change the number of requested rows for a table.
   * 
   * @param row - The affected row
   * @param newCount - The updated row count
   */
  changeRowCount(row: RowInclusionValidity, newCount: string) {
    const parsed = parseInt(newCount);
    row.rowCountValid = parsed > 0;
    if (parsed > 0) {
      row.row_count = parsed;
      this.emit();
    } else {
      this.requisitionChanged.emit();
    }
  }

  /**
   * Change the generator seed for a table.
   * 
   * @param row - The affected row
   * @param newSeed - The updated seed value
   */
  changeSeed(row: RowInclusionValidity, newSeed: string) {
    if (!newSeed) {
      row.seed = null;
      row.seedValid = true;
    } else {
      const parsed = parseInt(newSeed);
      row.seedValid = !isNaN(parsed);
      if (row.seedValid) {
        row.seed = parsed;
      }
    }
    if (row.seedValid) {
      this.emit();
    } else {
      this.requisitionChanged.emit();
    }
  }

  /**
   * Emit requistion change event.
   */
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
