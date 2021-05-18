import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { FormBuilder } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { of } from 'rxjs';
import { SnackService } from 'src/app/service/snack.service';
import { Mock, Spy } from 'src/app/test';
import { ColumnFacadeService } from '../../service/column-facade.service';

import { ColumnFormComponent, ColumnFormInput } from './column-form.component';

describe('ColumnFormComponent', () => {
  let component: ColumnFormComponent;
  let fixture: ComponentFixture<ColumnFormComponent>;

  const columnFacadeSpy = jasmine.createSpyObj(
    'ColumnFacadeService',
    ['createColumn', 'patchColumn']
  );

  const formBuilderSpy = new FormBuilder();
  const dialogRefSpy = Spy.dialogRef();
  const snackServiceSpy = Spy.snackService();
  const column = Mock.column();
  const tableId = 1;
  const data: ColumnFormInput = {
    table: {id: tableId},
    column: column
  };

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ ColumnFormComponent ],
      providers: [
        {provide: FormBuilder, useValue: formBuilderSpy},
        {provide: MatDialogRef, useValue: dialogRefSpy},
        {provide: MAT_DIALOG_DATA, useValue: data},
        {provide: ColumnFacadeService, useValue: columnFacadeSpy},
        {provide: SnackService, useValue: snackServiceSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ColumnFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should be in edit mode', () => {
    expect(component.editMode).toBeTruthy();
  });

  it('#colTypeDisabled should be true', () => {
    expect(component.colTypeDisabled).toBeTruthy();
  });

  it('should patch the column on submit', () => {
    columnFacadeSpy.patchColumn.and.returnValue(of(column));
    dialogRefSpy.close.and.returnValue();
    component.submit();
    expect(columnFacadeSpy.patchColumn).toHaveBeenCalledWith(
      tableId,
      column.id,
      {name: column.name, col_type: column.col_type, nullable: column.nullable}
    );
    expect(dialogRefSpy.close).toHaveBeenCalled();
    expect(columnFacadeSpy.createColumn).not.toHaveBeenCalled();
  });
});
