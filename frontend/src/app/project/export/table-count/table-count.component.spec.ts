import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TableCountComponent } from './table-count.component';

describe('TableCountComponent', () => {
  let component: TableCountComponent;
  let fixture: ComponentFixture<TableCountComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TableCountComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TableCountComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
