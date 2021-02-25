import { MatSnackBarConfig } from "@angular/material/snack-bar";

export namespace Snack {
  export const CONFIG: MatSnackBarConfig = {
    duration: 2000
  };
  export const OK = 'OK';
}

export namespace Constants {
  export const TOKEN_KEY = 'token';

  export const types = [
    'integer',
    'float',
    'bool',
    'string',
    'datetime'
  ];
}
