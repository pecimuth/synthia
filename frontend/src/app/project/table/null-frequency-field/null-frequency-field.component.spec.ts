import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { SnackService } from 'src/app/service/snack.service';
import { Spy } from 'src/app/test';
import { GeneratorFacadeService } from '../../service/generator-facade.service';

import { NullFrequencyFieldComponent } from './null-frequency-field.component';

describe('NullFrequencyFieldComponent', () => {
  let component: NullFrequencyFieldComponent;
  let fixture: ComponentFixture<NullFrequencyFieldComponent>;

  const generatorFacadeSpy = jasmine.createSpyObj(
    'GeneratorFacadeService',
    ['getGeneratorByName', 'patchParams']
  );

  const snackServiceSpy = Spy.snackService();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NullFrequencyFieldComponent ],
      providers: [
        {provide: SnackService, useValue: snackServiceSpy},
        {provide: GeneratorFacadeService, useValue: generatorFacadeSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NullFrequencyFieldComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
