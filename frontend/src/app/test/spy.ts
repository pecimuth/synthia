import { of } from "rxjs";
import { Mock } from "./mock";

export namespace Spy {
  /**
   * Create a spy for the SnackService, without any return
   * values for the methods.
   * 
   * @returns SnackService spy
   */
  export function snackService() {
    const snackServiceSpy = jasmine.createSpyObj(
      'SnackService',
      ['snack', 'errorIntoSnack']
    );
    return snackServiceSpy;
  }

  /** 
   * Create a spy for the ActiverProjectService, with the project$
   * property returning the (observable) mock project.
   * 
   * @returns ActiveProjectService spy
   */
  export function activeProjectObservableOnly() {
    const project = Mock.project();
    const activeProjectSpy = jasmine.createSpyObj(
      'ActiveProjectService',
      [],
      {'project$': of(project)}
    );
    return activeProjectSpy;
  }

  export function projectFacadeObservableOnly() {
    const projectList = Mock.projectList();
    const projectFacadeSpy = jasmine.createSpyObj(
      'ProjectFacadeService',
      [],
      {'list$': of(projectList)}
    );
    return projectFacadeSpy;
  }

  export function matDialog() {
    const dialogSpy = jasmine.createSpyObj(
      'MatDialog',
      ['open']
    );
    return dialogSpy;
  }

  export function blobDownloadService() {
    const blobDownloadSpy = jasmine.createSpyObj(
      'BlobDownloadService',
      ['handleResponse']
    );
    return blobDownloadSpy;
  }
}
