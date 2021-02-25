import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateColumnFormComponent } from './create-column-form.component';

describe('CreateColumnFormComponent', () => {
  let component: CreateColumnFormComponent;
  let fixture: ComponentFixture<CreateColumnFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CreateColumnFormComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateColumnFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
