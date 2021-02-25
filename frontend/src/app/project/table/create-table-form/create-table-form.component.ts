import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { TableCreate } from 'src/app/api/models/table-create';
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
    private activeProject: ActiveProjectService
  ) { }

  ngOnInit(): void {
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  onSubmit() {
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
      .subscribe(() => this.dialogRef.close());
  }
}
