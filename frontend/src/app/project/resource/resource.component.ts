import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { DataSourceView } from 'src/app/api/models/data-source-view';
import { DataSourceService } from 'src/app/api/services';
import { SnackService } from 'src/app/service/snack.service';
import { DataSourceFacadeService } from '../service/data-source-facade.service';

@Component({
  selector: 'app-resource',
  templateUrl: './resource.component.html',
  styleUrls: ['./resource.component.scss']
})
export class ResourceComponent implements OnInit, OnDestroy {

  @Input() dataSource: DataSourceView;

  private unsubscribe$ = new Subject();
  
  constructor(
    private dataSourceService: DataSourceService,
    private dataSourceFacade: DataSourceFacadeService,
    private snackService: SnackService
  ) { }

  ngOnInit(): void {
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  import() {
   this.dataSourceFacade.import(this.dataSource.id)
    .pipe(takeUntil(this.unsubscribe$))
    .subscribe(
      () => this.snackService.snack('Successfully imported the schema'),
      (err) => this.snackService.errorIntoSnack(err, 'Failed to import the schema')
    );
  }

  delete() {
    this.dataSourceFacade.delete(this.dataSource.id)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(
        () => null,
        (err) => this.snackService.errorIntoSnack(err, 'Failed to deleted the resource')
      );
  }

  download() {
    this.dataSourceFacade.download(this.dataSource.id)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(
        () => null,
        (err) => this.snackService.errorIntoSnack(err, 'Failed to download the file')
      );
  }
}
