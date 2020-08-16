import { Component, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { filter, distinctUntilChanged } from 'rxjs/operators';
import { AuthFacadeService } from './service/auth-facade.service';
import { ProjectFacadeService } from './service/project-facade.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnDestroy {

  private userSub: Subscription;

  constructor(
    private authFacade: AuthFacadeService,
    private projectFacade: ProjectFacadeService
  ) {}

  ngOnInit() {
    this.authFacade.refresh();
    this.userSub = this.authFacade.user$
      .pipe(filter((user) => !!user), distinctUntilChanged())
      .subscribe(() => this.projectFacade.refreshList());
  }

  ngOnDestroy() {
    if (this.userSub) {
      this.userSub.unsubscribe();
    }
    this.authFacade.complete();
    this.projectFacade.complete();
  }
}
