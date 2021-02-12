import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { MatCheckboxChange } from '@angular/material/checkbox';
import { ProjectView } from 'src/app/api/models/project-view';
import { TableCountsWrite } from 'src/app/api/models/table-counts-write';

const BASE_COUNT = 100;
type TableCount = {name: string, included: boolean, count: number};

@Component({
  selector: 'app-table-count',
  templateUrl: './table-count.component.html',
  styleUrls: ['./table-count.component.scss']
})
export class TableCountComponent implements OnInit {

  tableCountsFlat: Array<TableCount>;
  allIncluded = true;
  indeterminate = false;

  private _project: ProjectView;
  @Input() set project(newProject: ProjectView) {
    this._project = newProject;
    this.allIncluded = true;
    this.indeterminate = false;
    this.tableCountsFlat = newProject.tables
      .map((table) => {
        return {
          name: table.name,
          included: true,
          count: BASE_COUNT
        };
      });
    this.emit();
  }
  get project(): ProjectView {
    return this._project;
  }

  @Output() tableCountsChanged = new EventEmitter<TableCountsWrite>();

  displayedColumns = ['table', 'row_count'];

  constructor() { }

  ngOnInit(): void {}

  include(tableCount: TableCount, event: MatCheckboxChange) {
    tableCount.included = event.checked;
    this.allIncluded = tableCount.included && this.tableCountsFlat.every((other) => other.included);
    this.indeterminate = !this.allIncluded && this.tableCountsFlat.some((other) => other.included);
    this.emit();
  }

  includeAll(event: MatCheckboxChange) {
    this.allIncluded = event.checked;
    this.tableCountsFlat.forEach((tableCount) => tableCount.included = event.checked);
    this.indeterminate = false;
    this.emit();
  }

  changeRowCount(tableCount: TableCount, newCount: string) {
    tableCount.count = parseInt(newCount) || 0;
    this.emit();
  }

  private emit() {
    const tableCounts: TableCountsWrite = {
      rows_by_table_name: {}
    };
    this.tableCountsFlat.forEach(
      (item) => tableCounts.rows_by_table_name[item.name] = item.count
    );
    this.tableCountsChanged.emit(tableCounts);
  }
}
