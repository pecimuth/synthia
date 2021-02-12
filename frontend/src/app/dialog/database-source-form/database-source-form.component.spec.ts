import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DatabaseSourceFormComponent } from './database-source-form.component';

describe('DatabaseSourceFormComponent', () => {
  let component: DatabaseSourceFormComponent;
  let fixture: ComponentFixture<DatabaseSourceFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DatabaseSourceFormComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DatabaseSourceFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
