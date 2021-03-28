import { Component, OnInit, Input, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-page-header',
  templateUrl: './page-header.component.html',
  styleUrls: ['./page-header.component.scss']
})
export class PageHeaderComponent implements OnInit {

  /**
   * The main displayed text.
   */
  @Input() title: string;

  /**
   * Should the side navigation button be visible?
   */
  @Input() sidenavButton = false;

  /**
   * Event triggered when the navigation is toggled.
   * Triggered only with a side navigation button enabled.
   */
  @Output() toggleSidenav = new EventEmitter(); 

  constructor() { }

  ngOnInit(): void {
  }

  toggle() {
    this.toggleSidenav.emit();
  }
}
