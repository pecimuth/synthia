import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { MatDialog } from '@angular/material/dialog';
import { SnackService } from 'src/app/service/snack.service';
import { Spy } from 'src/app/test';
import { DataSourceFacadeService } from '../service/data-source-facade.service';

import { ResourceComponent } from './resource.component';

describe('ResourceComponent', () => {
  let component: ResourceComponent;
  let fixture: ComponentFixture<ResourceComponent>;
  const dialogSpy = Spy.matDialog();
  const snackServiceSpy = Spy.snackService();
  const dataSourceFacadeSpy = jasmine.createSpyObj(
    'DataSourceFacade',
    ['import', 'delete', 'download']
  );

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ ResourceComponent ],
      providers: [
        {provide: MatDialog, useValue: dialogSpy},
        {provide: SnackService, useValue: snackServiceSpy},
        {provide: DataSourceFacadeService, useValue: dataSourceFacadeSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ResourceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
