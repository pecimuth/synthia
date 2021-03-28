import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { TablePreviewComponent } from './table-preview.component';

describe('TablePreviewComponent', () => {
  let component: TablePreviewComponent;
  let fixture: ComponentFixture<TablePreviewComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ TablePreviewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TablePreviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
