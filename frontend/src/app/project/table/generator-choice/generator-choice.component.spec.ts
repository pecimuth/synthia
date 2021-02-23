import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GeneratorChoiceComponent } from './generator-choice.component';

describe('GeneratorChoiceComponent', () => {
  let component: GeneratorChoiceComponent;
  let fixture: ComponentFixture<GeneratorChoiceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GeneratorChoiceComponent ]
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
