import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { ExportRequisitionView } from 'src/app/api/models/export-requisition-view';
import { ExportRequisitionComponent } from './export-requisition.component';
import { Mock } from 'src/app/test/mock';

describe('ExportRequisitionComponent', () => {
  let component: ExportRequisitionComponent;
  let fixture: ComponentFixture<ExportRequisitionComponent>;

  beforeEach(waitForAsync(() => {
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

  it('should emit on project assignment', () => {
    const project = Mock.project();
    component.requisitionChanged.subscribe(
      (requisition: ExportRequisitionView) => {
        expect(requisition?.rows?.length).toBe(project.tables.length);
        requisition.rows.forEach(
          (row, index) => expect(row.table_name).toBe(project.tables[index].name)
        );
      }
    );
    component.project = project;
  });
});
