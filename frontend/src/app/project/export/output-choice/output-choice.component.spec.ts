import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { OutputFileDriverListView } from 'src/app/api/models/output-file-driver-list-view';
import { GeneratorService } from 'src/app/api/services';

import { OutputChoiceComponent } from './output-choice.component';

describe('OutputChoiceComponent', () => {
  let component: OutputChoiceComponent;
  let fixture: ComponentFixture<OutputChoiceComponent>;

  const generatorServiceSpy = jasmine.createSpyObj(
    'GeneratorService',
    ['getApiOutputFileDrivers']
  );

  const outputFileDrivers: OutputFileDriverListView = {
    items: [
      {driver_name: 'foo', display_name: 'Foo', mime_type: 'application/foo'},
      {driver_name: 'bar', display_name: 'Bar', mime_type: 'application/bar'}
    ]
  };
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
