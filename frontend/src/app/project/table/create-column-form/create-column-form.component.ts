import { Component, Inject, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ColumnCreate } from 'src/app/api/models/column-create';
import { Constants } from 'src/app/service/constants';
import { ColumnFacadeService } from '../../service/column-facade.service';

export interface CreateColumnFormInput {
  tableId: number
}

@Component({
  selector: 'app-create-column-form',
  templateUrl: './create-column-form.component.html',
  styleUrls: ['./create-column-form.component.scss']
})
export class CreateColumnFormComponent implements OnInit, OnDestroy {

  types = Constants.types;

  columnForm = this.fb.group({
    name: [null, Validators.required],
    col_type: ['string', Validators.required],
    nullable: [false, Validators.required]
  });

  private unsubscribe$ = new Subject();

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: CreateColumnFormInput,
    private dialogRef: MatDialogRef<CreateColumnFormComponent>,
    private columnFacade: ColumnFacadeService,
    private fb: FormBuilder
  ) { }

  ngOnInit(): void {
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  onSubmit() {
    const column: ColumnCreate = {
      ...this.columnForm.value,
      table_id: this.data.tableId
    };
    this.columnFacade.createColumn(column)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(() => this.dialogRef.close());
  }
}
