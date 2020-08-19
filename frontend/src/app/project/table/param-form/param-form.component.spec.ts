import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ParamFormComponent } from './param-form.component';

describe('ParamFormComponent', () => {
  let component: ParamFormComponent;
  let fixture: ComponentFixture<ParamFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ParamFormComponent ]
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
