import { Component, OnInit, OnDestroy } from '@angular/core';
import { AuthFacadeService } from 'src/app/service/auth-facade.service';
import { UserView } from 'src/app/api/models/user-view';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-user-menu',
  templateUrl: './user-menu.component.html',
  styleUrls: ['./user-menu.component.scss']
})
export class UserMenuComponent implements OnInit, OnDestroy {

  user: UserView;
  private userSub: Subscription;

  constructor(
    public authFacade: AuthFacadeService
  ) { }

  ngOnInit(): void {
    this.userSub = this.authFacade.user$
      .subscribe(
        (user) => this.user = user
      );
  }

  ngOnDestroy() {
    this.userSub.unsubscribe();
  }
}
