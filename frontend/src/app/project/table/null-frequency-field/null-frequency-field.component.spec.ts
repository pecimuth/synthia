import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NullFrequencyFieldComponent } from './null-frequency-field.component';

describe('NullFrequencyFieldComponent', () => {
  let component: NullFrequencyFieldComponent;
  let fixture: ComponentFixture<NullFrequencyFieldComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NullFrequencyFieldComponent ]
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
