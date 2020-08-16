import { Component, OnInit, Input, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-page-header',
  templateUrl: './page-header.component.html',
  styleUrls: ['./page-header.component.scss']
})
export class PageHeaderComponent implements OnInit {

  @Input() title: string;
  @Input() sidenavButton = false;
  @Output() toggleSidenav = new EventEmitter(); 

  constructor() { }

  ngOnInit(): void {
  }

  onClick() {
    this.toggleSidenav.emit();
  }
}
