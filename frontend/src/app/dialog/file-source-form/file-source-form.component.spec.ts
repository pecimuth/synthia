import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FileSourceFormComponent } from './file-source-form.component';

describe('FileSourceFormComponent', () => {
  let component: FileSourceFormComponent;
  let fixture: ComponentFixture<FileSourceFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FileSourceFormComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FileSourceFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
