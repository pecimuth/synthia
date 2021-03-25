import { TestBed } from '@angular/core/testing';
import { MatSnackBar } from '@angular/material/snack-bar';

import { SnackService } from './snack.service';

describe('SnackService', () => {
  let service: SnackService;

  const snackBarSpy = jasmine.createSpyObj(
    'MatSnackBar',
    ['open']
  );

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {provide: MatSnackBar, useValue: snackBarSpy}
      ]
    });
    service = TestBed.inject(SnackService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
