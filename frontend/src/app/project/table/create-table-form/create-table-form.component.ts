import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { TableCreate } from 'src/app/api/models/table-create';
import { SnackService } from 'src/app/service/snack.service';
import { ActiveProjectService } from '../../service/active-project.service';
import { TableFacadeService } from '../../service/table-facade.service';

@Component({
  selector: 'app-create-table-form',
  templateUrl: './create-table-form.component.html',
  styleUrls: ['./create-table-form.component.scss']
})
export class CreateTableFormComponent implements OnInit {

  tableForm = this.fb.group({
    name: [null, Validators.required]
  });

  private unsubscribe$ = new Subject();

  constructor(
    private dialogRef: MatDialogRef<CreateTableFormComponent>,
    private tableFacade: TableFacadeService,
    private fb: FormBuilder,
    private activeProject: ActiveProjectService,
    private snackService: SnackService
  ) { }

  ngOnInit(): void {
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  /**
   * Create the table via the API.
   */
  submit() {
    if (!this.tableForm.valid) {
      return;
    }
    const projectId = this.activeProject.project$.value.id;
    if (!projectId) {
      return;
    }
    const table: TableCreate = {
      ...this.tableForm.value,
      project_id: projectId
    };
    this.tableFacade.createTable(table)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(
        () => this.dialogRef.close(),
        (err) => this.snackService.errorIntoSnack(err)
      );
  }
}
