import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OutputChoiceComponent } from './output-choice.component';

describe('OutputChoiceComponent', () => {
  let component: OutputChoiceComponent;
  let fixture: ComponentFixture<OutputChoiceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OutputChoiceComponent ]
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
});
