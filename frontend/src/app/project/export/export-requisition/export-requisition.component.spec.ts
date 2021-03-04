import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ExportRequisitionComponent } from './export-requisition.component';

describe('ExportRequisitionComponent', () => {
  let component: ExportRequisitionComponent;
  let fixture: ComponentFixture<ExportRequisitionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ExportRequisitionComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ExportRequisitionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
