import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { GeneratorService } from 'src/app/api/services';
import { Mock } from 'src/app/test/mock';

import { OutputChoiceComponent } from './output-choice.component';

describe('OutputChoiceComponent', () => {
  let component: OutputChoiceComponent;
  let fixture: ComponentFixture<OutputChoiceComponent>;

  const generatorServiceSpy = jasmine.createSpyObj(
    'GeneratorService',
    ['getApiOutputFileDrivers']
  );

  const outputFileDrivers = Mock.outputFileDrivers();
  generatorServiceSpy.getApiOutputFileDrivers.and.returnValue(of(outputFileDrivers));

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OutputChoiceComponent ],
      providers: [
        {provide: GeneratorService, useValue: generatorServiceSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OutputChoiceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load output file drivers', () => {
    expect(component.fileDrivers).toBe(outputFileDrivers);
  });
});
