import { Component, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { filter, distinctUntilChanged } from 'rxjs/operators';
import { AuthFacadeService } from './service/auth-facade.service';
import { ProjectFacadeService } from './service/project-facade.service';
import { GeneratorFacadeService } from './service/generator-facade.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnDestroy {

  showMenu = false;
  private userSub: Subscription;

  constructor(
    private authFacade: AuthFacadeService,
    private projectFacade: ProjectFacadeService,
    private generatorFacade: GeneratorFacadeService
  ) {}

  ngOnInit() {
    this.authFacade.refresh();
    this.generatorFacade.refresh();
    this.userSub = this.authFacade.user$
      .subscribe((user) => {
        this.showMenu = !!user;
        if (user) {
          this.projectFacade.refreshList();
        }
      });
  }

  ngOnDestroy() {
    if (this.userSub) {
      this.userSub.unsubscribe();
    }
  }
}
