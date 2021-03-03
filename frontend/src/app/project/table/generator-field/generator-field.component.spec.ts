import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GeneratorFieldComponent } from './generator-field.component';

describe('GeneratorFieldComponent', () => {
  let component: GeneratorFieldComponent;
  let fixture: ComponentFixture<GeneratorFieldComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GeneratorFieldComponent ]
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
