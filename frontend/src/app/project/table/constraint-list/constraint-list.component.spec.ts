import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { ConstraintListComponent } from './constraint-list.component';

describe('ConstraintListComponent', () => {
  let component: ConstraintListComponent;
  let fixture: ComponentFixture<ConstraintListComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ ConstraintListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ConstraintListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
