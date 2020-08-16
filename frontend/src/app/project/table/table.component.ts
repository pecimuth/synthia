import { Component, OnInit } from '@angular/core';
import { Subscription, combineLatest } from 'rxjs';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss']
})
export class TableComponent implements OnInit {

  table: any;
  private tableSub: Subscription;

  constructor(
    private projectFacade: ProjectFacadeService,
    private activatedRoute: ActivatedRoute
  ) { }

  ngOnInit(): void {
    this.tableSub = combineLatest([
      this.activatedRoute.parent.params,
      this.activatedRoute.params,
      this.projectFacade.list$
    ]).subscribe(
      ([parent, params, list]) => {
        if (!list.items.length) {
          return;
        }
        const id = parseInt(parent.id);
        const tid = parseInt(params.tid);
        const project = list.items.find((item) => item.id === id);
        this.table = project.tables.find((item) => item.id === tid);
      }
    );
  }

  ngOnDestroy() {
    if (this.tableSub) {
      this.tableSub.unsubscribe();
    }
  }
}
