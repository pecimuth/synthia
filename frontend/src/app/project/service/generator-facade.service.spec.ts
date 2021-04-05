import { TestBed } from '@angular/core/testing';
import { GeneratorService } from 'src/app/api/services';
import { ActiveProjectService } from './active-project.service';

import { GeneratorFacadeService } from './generator-facade.service';

describe('GeneratorFacadeService', () => {
  let service: GeneratorFacadeService;

  const activeProjectSpy = jasmine.createSpyObj(
    'ActiveProjectService',
    [
      'patchGeneratorSetting',
      'deleteGeneratorSetting',
      'addGeneratorSetting'
    ],
    ['project$']
  );

  const generatorServiceSpy = jasmine.createSpyObj(
    'GeneratorService',
    [
      'getApiGenerators',
      'patchApiGeneratorSettingId',
      'deleteApiGeneratorSettingId',
      'postApiGeneratorSetting'
    ]
  );

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {provide: ActiveProjectService, useValue: activeProjectSpy},
        {provide: GeneratorService, useValue: generatorServiceSpy},
      ]
    });
    service = TestBed.inject(GeneratorFacadeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
