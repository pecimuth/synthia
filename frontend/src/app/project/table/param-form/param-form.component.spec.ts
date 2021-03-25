import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormBuilder } from '@angular/forms';
import { SnackService } from 'src/app/service/snack.service';
import { Spy } from 'src/app/test';
import { GeneratorFacadeService } from '../../service/generator-facade.service';

import { ParamFormComponent } from './param-form.component';

describe('ParamFormComponent', () => {
  let component: ParamFormComponent;
  let fixture: ComponentFixture<ParamFormComponent>;

  const generatorFacadeSpy = jasmine.createSpyObj(
    'GeneratorFacadeService',
    ['getGeneratorByName', 'patchParams']
  );

  const formBuilderSpy = Spy.formBuilder();
  formBuilderSpy.group.and.returnValue({controls: {}});

  const snackServiceSpy = Spy.snackService();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ParamFormComponent ],
      providers: [
        {provide: SnackService, useValue: snackServiceSpy},
        {provide: GeneratorFacadeService, useValue: generatorFacadeSpy},
        {provide: FormBuilder, useValue: formBuilderSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ParamFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
