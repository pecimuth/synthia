import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { ProjectView } from 'src/app/api/models/project-view';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { Mock } from 'src/app/test';
import { ActiveProjectService } from './active-project.service';


describe('ActiveProjectService', () => {
  let service: ActiveProjectService;

  let projectFacadeSpy: jasmine.SpyObj<ProjectFacadeService>;

  beforeEach(() => {
    projectFacadeSpy = jasmine.createSpyObj(
      'ProjectFacadeService',
      ['findById']
    );
    TestBed.configureTestingModule({
      providers: [
        {provide: ProjectFacadeService, useValue: projectFacadeSpy}
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
      projectFacadeSpy.findById.and.returnValue(of(project));
      service.projectId = project.id;
    });

    it('setting the project ID should find the project', () => {
      expect(projectFacadeSpy.findById).toHaveBeenCalledWith(project.id);
      expect(service.project$.value).toBe(project);
    });
  });  
});
