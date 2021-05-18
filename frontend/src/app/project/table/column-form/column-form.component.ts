import { Component, Inject, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ColumnView, ColumnWrite, TableView } from 'src/app/api/models';
import { ColumnCreate } from 'src/app/api/models/column-create';
import { Constants } from 'src/app/service/constants';
import { SnackService } from 'src/app/service/snack.service';
import { ColumnFacadeService } from '../../service/column-facade.service';

/**
 * Dialog input type.
 * 
 * The table must always be specified. Column is specified iff
 * we are editing it.
 */
export interface ColumnFormInput {
  table: TableView,
  column?: ColumnView
}

@Component({
  selector: 'app-column-form',
  templateUrl: './column-form.component.html',
  styleUrls: ['./column-form.component.scss']
})
export class ColumnFormComponent implements OnInit, OnDestroy {

  /**
   * List of available value types.
   */
  types = Constants.types;

  columnForm = this.fb.group({
    name: [null, Validators.required],
    col_type: ['string', Validators.required],
    nullable: [false, Validators.required]
  });

  /**
   * If a column is specified, we are in edit mode.
   * Otherwise we are creating a new column.
   */
  editMode: boolean;

  /**
   * Is the column type input disabled?
   * 
   * Should be disabled in edit mode, when the column is imported
   * or has a generator assigned.
   */
  colTypeDisabled: boolean;

  private unsubscribe$ = new Subject();

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: ColumnFormInput,
    private dialogRef: MatDialogRef<ColumnFormComponent>,
    private columnFacade: ColumnFacadeService,
    private fb: FormBuilder,
    private snackService: SnackService
  ) { }

  ngOnInit(): void {
    this.editMode = !!this.data.column;
    if (this.editMode) {
      this.columnForm.setValue({
        name: this.data.column.name,
        col_type: this.data.column.col_type,
        nullable: this.data.column.nullable
      });
    }
    this.colTypeDisabled = this.editMode && !!(
      this.data.column.reflected_column_idf || this.data.column.generator_setting
    );
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  /**
   * If we do not have a column specified, create it via the API.
   * If we have a column specified, patch it via the API.
   */
  submit() {
    if (!this.columnForm.valid) {
      return;
    }

    if (this.data.column) {
      const column: ColumnWrite = {
        ...this.columnForm.value
      };
      this.columnFacade.patchColumn(this.data.table.id, this.data.column.id, column)
        .pipe(takeUntil(this.unsubscribe$))
        .subscribe(
          () => this.dialogRef.close(),
          (err) => this.snackService.errorIntoSnack(err)
        );
      return;
    }

    const column: ColumnCreate = {
      ...this.columnForm.value,
      table_id: this.data.table.id
    };
    this.columnFacade.createColumn(column)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(
        () => this.dialogRef.close(),
        (err) => this.snackService.errorIntoSnack(err)
      );
  }
}
