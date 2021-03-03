import { Component, OnInit } from '@angular/core';
import { Validators, FormBuilder } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { DataSourceFacadeService } from 'src/app/project/service/data-source-facade.service';
import { SnackService } from 'src/app/service/snack.service';
import { CreateProjectFormComponent } from '../create-project-form/create-project-form.component';

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
    private dialogRef: MatDialogRef<CreateProjectFormComponent>,
    private dataSourceFacade: DataSourceFacadeService,
    private snackService: SnackService
  ) {}

  ngOnInit() {}

  onSubmit() {
    this.dataSourceFacade.createDatabase(this.databaseForm.value)
      .subscribe(
        () => this.dialogRef.close(),
        (err) => this.snackService.errorIntoSnack(err, 'Failed to add a database')
      );
  }
}
