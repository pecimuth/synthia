import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { MatDialog } from '@angular/material/dialog';
import { SnackService } from 'src/app/service/snack.service';
import { Spy } from 'src/app/test';
import { ActiveProjectService } from '../../service/active-project.service';
import { DataSourceFacadeService } from '../../service/data-source-facade.service';

import { ResourceListComponent } from './resource-list.component';

describe('ResourceListComponent', () => {
  let component: ResourceListComponent;
  let fixture: ComponentFixture<ResourceListComponent>;
  const dialogSpy = Spy.matDialog();
  const activeProjectSpy = Spy.activeProjectObservableOnly();
  const snackServiceSpy = Spy.snackService();
  const dataSourceFacadeSpy = jasmine.createSpyObj(
    'DataSourceFacade',
    ['mockDatabase']
  );

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ ResourceListComponent ],
      providers: [
        {provide: MatDialog, useValue: dialogSpy},
        {provide: ActiveProjectService, useValue: activeProjectSpy},
        {provide: SnackService, useValue: snackServiceSpy},
        {provide: DataSourceFacadeService, useValue: dataSourceFacadeSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ResourceListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
