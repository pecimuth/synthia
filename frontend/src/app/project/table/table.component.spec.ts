import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { MatDialog } from '@angular/material/dialog';
import { SnackService } from 'src/app/service/snack.service';
import { Spy } from 'src/app/test';
import { ColumnFacadeService } from '../service/column-facade.service';
import { TableFacadeService } from '../service/table-facade.service';

import { TableComponent } from './table.component';

describe('TableComponent', () => {
  let component: TableComponent;
  let fixture: ComponentFixture<TableComponent>;

  const tableFacadeSpy = jasmine.createSpyObj(
    'TableFacadeService',
    ['deleteTable']
  );
 
  const columnFacadeSpy = jasmine.createSpyObj(
    'ColumnFacadeService',
    ['deleteColumn']
  );

  const dialogSpy = Spy.matDialog();
  const snackServiceSpy = Spy.snackService();

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ TableComponent ],
      providers: [
        {provide: MatDialog, useValue: dialogSpy},
        {provide: TableFacadeService, useValue: tableFacadeSpy},
        {provide: ColumnFacadeService, useValue: columnFacadeSpy},
        {provide: SnackService, useValue: snackServiceSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
