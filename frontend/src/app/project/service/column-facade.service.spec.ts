import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { ColumnWrite } from 'src/app/api/models';
import { ColumnService } from 'src/app/api/services';
import { Mock } from 'src/app/test/mock';
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
        {provide: ActiveProjectService, useValue: activeProjectSpy},
        {provide: ColumnService, useValue: columnServiceSpy},
      ]
    });
    service = TestBed.inject(ColumnFacadeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('#patchColumn should call the API and update the project state', () => {
    const tableId = 1;
    const columnId = 2;
    const columnWrite: ColumnWrite = {nullable: true};
    const column = Mock.column();
    columnServiceSpy.patchApiColumnId.and.returnValue(of(column));
    activeProjectSpy.patchColumn.and.returnValue(of(column));
    service.patchColumn(tableId, columnId, columnWrite).subscribe();
    expect(columnServiceSpy.patchApiColumnId).toHaveBeenCalledWith({id: columnId, column: columnWrite});
    expect(activeProjectSpy.patchColumn).toHaveBeenCalledWith(tableId, column);
  });
});
