import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GeneratorSelectComponent } from './generator-select.component';

describe('GeneratorSelectComponent', () => {
  let component: GeneratorSelectComponent;
  let fixture: ComponentFixture<GeneratorSelectComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GeneratorSelectComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GeneratorSelectComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
