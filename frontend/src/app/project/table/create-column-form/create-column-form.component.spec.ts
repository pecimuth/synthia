import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { FormBuilder } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { SnackService } from 'src/app/service/snack.service';
import { Spy } from 'src/app/test';
import { ColumnFacadeService } from '../../service/column-facade.service';

import { CreateColumnFormComponent, CreateColumnFormInput } from './create-column-form.component';

describe('CreateColumnFormComponent', () => {
  let component: CreateColumnFormComponent;
  let fixture: ComponentFixture<CreateColumnFormComponent>;

  const columnFacadeSpy = jasmine.createSpyObj(
    'ColumnFacadeService',
    ['createColumn']
  );

  const formBuilderSpy = Spy.formBuilder();
  formBuilderSpy.group.and.returnValue({controls: {}});

  const dialogRefSpy = Spy.dialogRef();
  const snackServiceSpy = Spy.snackService();
  const data: CreateColumnFormInput = {
    tableId: 1
  };

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ CreateColumnFormComponent ],
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
    fixture = TestBed.createComponent(CreateColumnFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
