import { Component, Input, OnInit } from '@angular/core';
import { TableView } from 'src/app/api/models/table-view';

@Component({
  selector: 'app-constraint-list',
  templateUrl: './constraint-list.component.html',
  styleUrls: ['./constraint-list.component.scss']
})
export class ConstraintListComponent implements OnInit {

  /**
   * The table for whose constraints we are responsible.
   */
  @Input() table: TableView;

  constructor() { }

  ngOnInit(): void {
  }
}
