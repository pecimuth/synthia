import { TestBed } from '@angular/core/testing';
import { ColumnService } from 'src/app/api/services';
import { ActiveProjectService } from './active-project.service';

import { ColumnFacadeService } from './column-facade.service';

describe('ColumnFacadeService', () => {
  let service: ColumnFacadeService;
  const activeProjectSpy = jasmine.createSpyObj(
    'ActiveProjectService',
    ['patchColumn', 'addColumn'],
    ['project$']
  );

  const columnServiceSpy = jasmine.createSpyObj(
    'ColumnService',
    ['patchApiColumnId', 'postApiColumn', 'deleteApiColumnId']
  );

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        ColumnFacadeService,
        {provide: ActiveProjectService, useValue: activeProjectSpy},
        {provide: ColumnService, useValue: columnServiceSpy},
      ]
    });
    service = TestBed.inject(ColumnFacadeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
