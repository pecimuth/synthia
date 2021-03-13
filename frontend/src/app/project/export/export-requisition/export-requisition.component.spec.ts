import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { ExportRequisitionView } from 'src/app/api/models/export-requisition-view';
import { ProjectView } from 'src/app/api/models/project-view';

import { ExportRequisitionComponent } from './export-requisition.component';

describe('ExportRequisitionComponent', () => {
  let component: ExportRequisitionComponent;
  let fixture: ComponentFixture<ExportRequisitionComponent>;

  const project: ProjectView = {
    tables: [
      {name: 'Foo'},
      {name: 'Bar'},
      {name: 'Baz'}
    ]
  };

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

  it('should emit on project assignment', () => {
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
