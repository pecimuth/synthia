import { Component, OnDestroy } from '@angular/core';
import { Subject } from 'rxjs';
import { AuthFacadeService } from './service/auth-facade.service';
import { ProjectFacadeService } from './service/project-facade.service';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnDestroy {

  /**
   * Should the menu be shown?
   */
  showMenu = false;

  private unsubscribe$ = new Subject();

  constructor(
    private authFacade: AuthFacadeService,
    private projectFacade: ProjectFacadeService
  ) {}

  ngOnInit() {
    this.authFacade.refresh();
    this.authFacade.user$
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe((user) => {
        this.showMenu = !!user;
        this.projectFacade.projects$.next(null);
        if (user) {
          this.projectFacade.refresh();
        }
      });
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }
}
