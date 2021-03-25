import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { MatDialog } from '@angular/material/dialog';
import { Spy } from 'src/app/test';
import { GeneratorFacadeService } from '../../service/generator-facade.service';

import { GeneratorFieldComponent } from './generator-field.component';

describe('GeneratorFieldComponent', () => {
  let component: GeneratorFieldComponent;
  let fixture: ComponentFixture<GeneratorFieldComponent>;

  const generatorFacadeSpy = jasmine.createSpyObj(
    'GeneratorFacadeService',
    ['isMultiColumn']
  );

  const dialogSpy = Spy.matDialog();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GeneratorFieldComponent ],
      providers: [
        {provide: MatDialog, useValue: dialogSpy},
        {provide: GeneratorFacadeService, useValue: generatorFacadeSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GeneratorFieldComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
