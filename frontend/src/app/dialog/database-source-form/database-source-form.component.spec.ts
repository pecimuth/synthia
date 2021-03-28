import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { FormBuilder } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { DataSourceFacadeService } from 'src/app/project/service/data-source-facade.service';
import { SnackService } from 'src/app/service/snack.service';
import { Mock, Spy } from 'src/app/test';

import { DatabaseSourceFormComponent } from './database-source-form.component';

describe('DatabaseSourceFormComponent', () => {
  let component: DatabaseSourceFormComponent;
  let fixture: ComponentFixture<DatabaseSourceFormComponent>;

  const dataSourceFacadeSpy = jasmine.createSpyObj(
    'DataSourceFacadeService',
    ['patchDatabase', 'createDatabase']
  );

  const formBuilderSpy = Spy.formBuilder();
  formBuilderSpy.group.and.returnValue({controls: {}});

  const dialogRefSpy = Spy.dialogRef();
  const dataSource = Mock.dataSourceDatabase();
  const snackServiceSpy = Spy.snackService();

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ DatabaseSourceFormComponent ],
      providers: [
        {provide: FormBuilder, useValue: formBuilderSpy},
        {provide: MatDialogRef, useValue: dialogRefSpy},
        {provide: MAT_DIALOG_DATA, useValue: dataSource},
        {provide: DataSourceFacadeService, useValue: dataSourceFacadeSpy},
        {provide: SnackService, useValue: snackServiceSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DatabaseSourceFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
