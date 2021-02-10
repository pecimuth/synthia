import { Component, Input, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { TableView } from 'src/app/api/models/table-view';
import { ColumnView } from 'src/app/api/models/column-view';
import { ActiveProjectService } from '../service/active-project.service';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss']
})
export class TableComponent implements OnInit {

  @Input() table: TableView;
  displayedColumns = ['column', 'generator', 'parameters', 'action'];

  constructor() { }

  ngOnInit() {}

  trackById = (index: number, item: ColumnView) => item.id;
}
