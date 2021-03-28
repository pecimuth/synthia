import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { FormBuilder } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { SnackService } from 'src/app/service/snack.service';
import { Spy } from 'src/app/test';
import { ActiveProjectService } from '../../service/active-project.service';
import { TableFacadeService } from '../../service/table-facade.service';

import { CreateTableFormComponent } from './create-table-form.component';

describe('CreateTableFormComponent', () => {
  let component: CreateTableFormComponent;
  let fixture: ComponentFixture<CreateTableFormComponent>;

  const tableFacadeSpy = jasmine.createSpyObj(
    'TableFacadeService',
    ['createTable']
  );

  const formBuilderSpy = Spy.formBuilder();
  formBuilderSpy.group.and.returnValue({controls: {}});

  const dialogRefSpy = Spy.dialogRef();
  const snackServiceSpy = Spy.snackService();
  const activeProjectSpy = Spy.activeProjectObservableOnly();

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ CreateTableFormComponent ],
      providers: [
        {provide: FormBuilder, useValue: formBuilderSpy},
        {provide: MatDialogRef, useValue: dialogRefSpy},
        {provide: TableFacadeService, useValue: tableFacadeSpy},
        {provide: SnackService, useValue: snackServiceSpy},
        {provide: ActiveProjectService, useValue: activeProjectSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateTableFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
