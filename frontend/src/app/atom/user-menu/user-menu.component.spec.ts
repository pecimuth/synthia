import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { MatMenuModule } from '@angular/material/menu';
import { of } from 'rxjs';
import { AuthFacadeService } from 'src/app/service/auth-facade.service';
import { SnackService } from 'src/app/service/snack.service';
import { Mock, Spy } from 'src/app/test';

import { UserMenuComponent } from './user-menu.component';

describe('UserMenuComponent', () => {
  let component: UserMenuComponent;
  let fixture: ComponentFixture<UserMenuComponent>;

  const matDialogSpy = Spy.matDialog();
  const routerSpy = Spy.router();
  const snackServiceSpy = Spy.snackService();
  const user = Mock.user();
  const authFacadeSpy = jasmine.createSpyObj(
    'AuthFacadeService',
    ['logout'],
    {'user$': of(user)}
  );

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ UserMenuComponent ],
      imports: [
        MatMenuModule
      ],
      providers: [
        {provide: Router, useValue: routerSpy},
        {provide: AuthFacadeService, useValue: authFacadeSpy},
        {provide: SnackService, useValue: snackServiceSpy},
        {provide: MatDialog, useValue: matDialogSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UserMenuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
