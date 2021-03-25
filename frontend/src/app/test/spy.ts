import { of } from "rxjs";
import { Mock } from "./mock";

/**
 * Create spy services for testing purposes.
 */
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
   * Create a spy for the ActiveProjectService, with the project$
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

  export function authFacadeObservableOnly() {
    const user = Mock.user();
    const authFacadeSpy = jasmine.createSpyObj(
      'AuthFacadeService',
      [],
      {'user$': of(user)}
    );
    return authFacadeSpy;
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

  export function router() {
    const routerSpy = jasmine.createSpyObj(
      'Router',
      ['navigateByUrl', 'navigate']
    );
    return routerSpy;
  }

  export function formBuilder() {
    const formBuilderSpy = jasmine.createSpyObj(
      'FormBuilder',
      ['group']
    );
    return formBuilderSpy;
  }

  export function dialogRef() {
    const dialogRefSpy = jasmine.createSpyObj(
      'MatDialogRef',
      ['close']
    );
    return dialogRefSpy;
  }
}
