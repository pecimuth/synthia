import { TestBed } from '@angular/core/testing';
import { TableService } from 'src/app/api/services';
import { ActiveProjectService } from './active-project.service';

import { TableFacadeService } from './table-facade.service';

describe('TableFacadeService', () => {
  let service: TableFacadeService;

  const activeProjectSpy = jasmine.createSpyObj(
    'ActiveProjectService',
    ['nextProject'],
    {'project$': null}
  );

  const tableServiceSpy = jasmine.createSpyObj(
    'TableService',
    [
      'deleteApiTable',
      'postApiTable'
    ]
  );

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {provide: ActiveProjectService, useValue: activeProjectSpy},
        {provide: TableService, useValue: tableServiceSpy},
      ]
    });
    service = TestBed.inject(TableFacadeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
