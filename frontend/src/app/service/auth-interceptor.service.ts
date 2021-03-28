import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Constants } from './constants';

@Injectable()
export class AuthInterceptorService implements HttpInterceptor {

  constructor() { }

  /**
   * Intercept API requests with the authorization token from the local storage.
   * 
   * @param request - API request
   * @param next - The next request handler
   * @returns Observable of the HTTP event
   */
  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {    
    const token = localStorage.getItem(Constants.TOKEN_KEY);
    if (token !== null) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });
    }
    return next.handle(request);
  }
}
