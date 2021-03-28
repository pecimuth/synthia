import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Snack } from './constants';

@Injectable({
  providedIn: 'root'
})
export class SnackService {

  constructor(private snackBar: MatSnackBar) { }

  /**
   * Show a snack bar with a custom message.
   * 
   * @param message - The text of the message
   */
  snack(message: string) {
    this.snackBar.open(message, Snack.OK, Snack.CONFIG);
  }

  /**
   * Show an error snack bar with a custom message.
   * 
   * @param message - The error message
   */
  errorSnack(message: string) {
    this.snackBar.open(message, Snack.OK, Snack.ERROR_CONFIG);
  }

  /**
   * Show an error snack bar after a failed API request.
   * 
   * @param err - Object that may containt a MessageView with an error message
   * @param defaultMessage - The error message displayed when err
   * does not contain an error message
   */
  errorIntoSnack(err: any, defaultMessage: string = 'An error occured') {
    if (err?.error?.message) {
      this.errorSnack(err.error.message);
    } else {
      this.errorSnack(defaultMessage);
    }
  }
}
