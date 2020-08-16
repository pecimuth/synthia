import { Component, OnInit, OnDestroy } from '@angular/core';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { ProjectView } from 'src/app/api/models/project-view';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-project-list',
  templateUrl: './project-list.component.html',
  styleUrls: ['./project-list.component.scss']
})
export class ProjectListComponent implements OnInit, OnDestroy {

  projects: ProjectView[];
  private projectsSub: Subscription;

  constructor(
    private projectFacade: ProjectFacadeService
  ) { }

  ngOnInit(): void {
    this.projectsSub = this.projectFacade.list$
      .subscribe(
        (projects) => this.projects = projects.items
      );
  }

  ngOnDestroy() {
    if (this.projectsSub) {
      this.projectsSub.unsubscribe();
    }
  }
}
