import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { MatDialogRef } from '@angular/material/dialog';
import { DataSourceFacadeService } from 'src/app/project/service/data-source-facade.service';
import { SnackService } from 'src/app/service/snack.service';
import { Spy } from 'src/app/test';

import { FileSourceFormComponent } from './file-source-form.component';

describe('FileSourceFormComponent', () => {
  let component: FileSourceFormComponent;
  let fixture: ComponentFixture<FileSourceFormComponent>;

  const dataSourceFacadeSpy = jasmine.createSpyObj(
    'DataSourceFacadeService',
    ['createFileDataSource']
  );

  const dialogRefSpy = Spy.dialogRef();
  const snackServiceSpy = Spy.snackService();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FileSourceFormComponent ],
      providers: [
        {provide: MatDialogRef, useValue: dialogRefSpy},
        {provide: DataSourceFacadeService, useValue: dataSourceFacadeSpy},
        {provide: SnackService, useValue: snackServiceSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FileSourceFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
