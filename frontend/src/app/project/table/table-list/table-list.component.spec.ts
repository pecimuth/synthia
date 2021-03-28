import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { MatDialog } from '@angular/material/dialog';
import { Spy } from 'src/app/test';
import { ActiveProjectService } from '../../service/active-project.service';

import { TableListComponent } from './table-list.component';

describe('TableListComponent', () => {
  let component: TableListComponent;
  let fixture: ComponentFixture<TableListComponent>;

  const activeProjectSpy = Spy.activeProjectObservableOnly();
  const dialogSpy = Spy.matDialog();

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ TableListComponent ],
      providers: [
        {provide: ActiveProjectService, useValue: activeProjectSpy},
        {provide: MatDialog, useValue: dialogSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TableListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
