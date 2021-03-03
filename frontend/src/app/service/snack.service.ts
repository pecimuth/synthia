import { HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Snack } from './constants';

@Injectable({
  providedIn: 'root'
})
export class SnackService {

  constructor(private snackBar: MatSnackBar) { }

  errorIntoSnack(err: any, defaultMessage: string = 'An error occured') {
    if (err instanceof HttpErrorResponse && err.error.message) {
      this.snackBar.open(err.error.message, Snack.OK, Snack.CONFIG);
    } else {
      this.snackBar.open(defaultMessage, Snack.OK, Snack.CONFIG);
    }
  }
}
