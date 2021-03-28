import { MatSnackBarConfig } from "@angular/material/snack-bar";

export namespace Snack {
  /**
   * Configuration of a snack bar
   */
  export const CONFIG: MatSnackBarConfig = {
    duration: 4000
  };

  /**
   * Configuration of a snack bar that show an error
   */
  export const ERROR_CONFIG: MatSnackBarConfig = {
    duration: 10000
  };

  /**
   * Snack bar button label
   */
  export const OK = 'OK';
}

export namespace Constants {
  /**
   * The localStorage key for the auth token
   */
  export const TOKEN_KEY = 'token';

  /**
   * List of value type names
   */
  export const types = [
    'integer',
    'float',
    'bool',
    'string',
    'datetime'
  ];
}
