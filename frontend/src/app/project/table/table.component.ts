import { Component, OnInit } from '@angular/core';
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

  table: TableView;
  private unsubscribe$ = new Subject();

  constructor(
    private activeProject: ActiveProjectService,
    private activatedRoute: ActivatedRoute
  ) { }

  ngOnInit(): void {
    this.activatedRoute.params
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe((params) => {
        this.activeProject.tableId = parseInt(params.tid);
      });
    this.activeProject.table$
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe((table) => this.table = table);
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  trackById = (index: number, item: ColumnView) => item.id;
}
