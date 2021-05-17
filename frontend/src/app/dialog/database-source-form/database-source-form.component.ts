import { Component, Inject, OnInit } from '@angular/core';
import { Validators, FormBuilder } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { DataSourceView } from 'src/app/api/models/data-source-view';
import { DataSourceFacadeService } from 'src/app/project/service/data-source-facade.service';
import { SnackService } from 'src/app/service/snack.service';
import { ProjectFormComponent } from '../project-form/project-form.component';

@Component({
  selector: 'app-database-source-form',
  templateUrl: './database-source-form.component.html',
  styleUrls: ['./database-source-form.component.scss']
})
export class DatabaseSourceFormComponent implements OnInit {

  databaseForm = this.fb.group({
    driver: ['postgresql', Validators.required],
    usr: [null, Validators.required],
    pwd: [null, Validators.required],
    host: [null, Validators.required],
    port: [null, Validators.required],
    db: [null, Validators.required]
  });

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<ProjectFormComponent>,
    private dataSourceFacade: DataSourceFacadeService,
    private snackService: SnackService,
    @Inject(MAT_DIALOG_DATA) public dataSource: DataSourceView,
  ) {}

  ngOnInit() {
    if (!this.dataSource) {
      return;
    }
    for (const [name, control] of Object.entries(this.databaseForm.controls)) {
      if (this.dataSource[name]) {
        control.setValue(this.dataSource[name]);
      }
    }
  }

  /**
   * Update or create the database data source.
   */
  submit() {
    this.touchAll();
    if (!this.databaseForm.valid) {
      return;
    }
    if (this.dataSource) {
      this.dataSourceFacade.patchDatabase(this.dataSource.id, this.databaseForm.value)
        .subscribe(
          () => this.dialogRef.close(),
          (err) => this.snackService.errorIntoSnack(err, 'Failed to update the resource')
        );
      return;
    }
    this.dataSourceFacade.createDatabase(this.databaseForm.value)
      .subscribe(
        () => this.dialogRef.close(),
        (err) => this.snackService.errorIntoSnack(err, 'Failed to add a database')
      );
  }

  /**
   * Mark all form controls as touched. This forces validation to take place.
   */
  private touchAll() {
    Object.values(this.databaseForm.controls)
      .forEach((control) => control.markAsTouched());
  }
}
