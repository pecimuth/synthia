import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { TableView, TableWrite } from 'src/app/api/models';
import { TableCreate } from 'src/app/api/models/table-create';
import { SnackService } from 'src/app/service/snack.service';
import { ActiveProjectService } from '../../service/active-project.service';
import { TableFacadeService } from '../../service/table-facade.service';

@Component({
  selector: 'app-table-form',
  templateUrl: './table-form.component.html',
  styleUrls: ['./table-form.component.scss']
})
export class TableFormComponent implements OnInit {

  tableForm = this.fb.group({
    name: [null, Validators.required]
  });

  private unsubscribe$ = new Subject();

  constructor(
    private dialogRef: MatDialogRef<TableFormComponent>,
    private tableFacade: TableFacadeService,
    private fb: FormBuilder,
    private activeProject: ActiveProjectService,
    private snackService: SnackService,
    @Inject(MAT_DIALOG_DATA) public data: TableView
  ) { }

  ngOnInit(): void {
    if (this.data) {
      this.tableForm.controls.name.setValue(this.data.name);
    }
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  /**
   * If we do not have a table specified, create it via the API.
   * If we have a table specified, patch it via the API.
   */
  submit() {
    if (!this.tableForm.valid) {
      return;
    }
    const projectId = this.activeProject.project$.value.id;
    if (!projectId) {
      return;
    }

    if (this.data) {
      const table: TableWrite = {
        name: this.tableForm.value['name']
      };
      this.tableFacade.patchTable(this.data.id, table)
        .pipe(takeUntil(this.unsubscribe$))
        .subscribe(
          () => this.dialogRef.close(),
          (err) => this.snackService.errorIntoSnack(err)
        );
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
