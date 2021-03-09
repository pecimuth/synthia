import { HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Snack } from './constants';

@Injectable({
  providedIn: 'root'
})
export class SnackService {

  constructor(private snackBar: MatSnackBar) { }

  snack(message: string) {
    this.snackBar.open(message, Snack.OK, Snack.CONFIG);
  }

  errorIntoSnack(err: any, defaultMessage: string = 'An error occured') {
    if (err?.error?.message) {
      this.snack(err.error.message);
    } else {
      this.snack(defaultMessage);
    }
  }
}
