import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { of } from 'rxjs';
import { ProjectService } from 'src/app/api/services';
import { Mock, Spy } from 'src/app/test';
import { ActiveProjectService } from '../service/active-project.service';

import { PreviewComponent } from './preview.component';

describe('PreviewComponent', () => {
  let component: PreviewComponent;
  let fixture: ComponentFixture<PreviewComponent>;

  const activeProjectSpy = Spy.activeProjectObservableOnly();
  
  const projectServiceSpy = jasmine.createSpyObj(
    'ProjectService',
    ['postApiProjectIdPreview']
  );

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ PreviewComponent ],
      providers: [
        {provide: ActiveProjectService, useValue: activeProjectSpy},
        {provide: ProjectService, useValue: projectServiceSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PreviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should fetch the preview', () => {
    const preview = Mock.preview();
    projectServiceSpy.postApiProjectIdPreview.and.returnValue(of(preview));
    component.ngOnInit();
    expect(component.preview).toBe(preview);
  });
});
