import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { ProjectView } from 'src/app/api/models/project-view';
import { ProjectService } from 'src/app/api/services';
import { Mock } from 'src/app/test';
import { ActiveProjectService } from './active-project.service';


describe('ActiveProjectService', () => {
  let service: ActiveProjectService;

  let projectServiceSpy: jasmine.SpyObj<ProjectService>;

  beforeEach(() => {
    projectServiceSpy = jasmine.createSpyObj(
      'ProjectService',
      ['getApiProjectId']
    );
    TestBed.configureTestingModule({
      providers: [
        {provide: ProjectService, useValue: projectServiceSpy}
      ]
    });
    service = TestBed.inject(ActiveProjectService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('active project CRUD operations', () => {
    let project: ProjectView;
    
    beforeEach(() => {
      project = Mock.project();
      projectServiceSpy.getApiProjectId.and.returnValue(of(project));
      service.projectId = project.id;
    });

    it('setting the project ID should fetch the project from API', () => {
      expect(projectServiceSpy.getApiProjectId).toHaveBeenCalledWith(project.id);
      expect(service.project$.value).toBe(project);
    });
  });  
});
