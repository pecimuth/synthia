export namespace Spy {
  export function snackService() {
    const snackServiceSpy = jasmine.createSpyObj(
      'SnackService',
      ['snack', 'errorIntoSnack']
    );
    return snackServiceSpy;
  }
}
