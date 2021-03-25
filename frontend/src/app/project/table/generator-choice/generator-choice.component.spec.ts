import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { of } from 'rxjs';
import { SnackService } from 'src/app/service/snack.service';
import { Mock, Spy } from 'src/app/test';
import { ActiveProjectService } from '../../service/active-project.service';
import { ColumnFacadeService } from '../../service/column-facade.service';
import { GeneratorFacadeService } from '../../service/generator-facade.service';

import { GeneratorChoiceComponent, GeneratorChoiceInput } from './generator-choice.component';

describe('GeneratorChoiceComponent', () => {
  let component: GeneratorChoiceComponent;
  let fixture: ComponentFixture<GeneratorChoiceComponent>;

  const generatorFacadeSpy = jasmine.createSpyObj(
    'GeneratorFacadeService',
    [
      'getGeneratorsForColumnByCategory',
      'deleteSetting',
      'isMultiColumn',
      'createSetting',
      'patchGeneratorName'
    ]
  );
  const generatorForColumnByCategory = [{}, []];
  generatorFacadeSpy.getGeneratorsForColumnByCategory.and
    .returnValue(of(generatorForColumnByCategory));
 
  const columnFacadeSpy = jasmine.createSpyObj(
    'ColumnFacadeService',
    ['setColumnGeneratorSetting']
  );

  const project = Mock.project();
  const table = project.tables[0];
  const column = table.columns[0];

  const activeProjectSpy = jasmine.createSpyObj(
    'ActiveProjectService',
    ['getTableColumn'],
    {'project$': of(project)}
  );
  activeProjectSpy.getTableColumn.and.returnValue(of([table, column]));

  const dialogRefSpy = Spy.dialogRef();
  const snackServiceSpy = Spy.snackService();
  const data: GeneratorChoiceInput = {
    columnId: column.id,
    tableId: table.id
  };

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GeneratorChoiceComponent ],
      providers: [
        {provide: MatDialogRef, useValue: dialogRefSpy},
        {provide: GeneratorFacadeService, useValue: generatorFacadeSpy},
        {provide: ColumnFacadeService, useValue: columnFacadeSpy},
        {provide: SnackService, useValue: snackServiceSpy},
        {provide: ActiveProjectService, useValue: activeProjectSpy},
        {provide: MAT_DIALOG_DATA, useValue: data}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GeneratorChoiceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
