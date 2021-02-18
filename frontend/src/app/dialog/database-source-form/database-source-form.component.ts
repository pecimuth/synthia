import { Component, OnInit } from '@angular/core';
import { Validators, FormBuilder } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { ResourceService } from 'src/app/project/service/resource.service';
import { CreateProjectFormComponent } from '../create-project-form/create-project-form.component';

@Component({
  selector: 'app-database-source-form',
  templateUrl: './database-source-form.component.html',
  styleUrls: ['./database-source-form.component.scss']
})
export class DatabaseSourceFormComponent implements OnInit {

  databaseForm = this.fb.group({
    driver: [{value: 'postgresql'}, Validators.required],
    usr: [null, Validators.required],
    pwd: [null, Validators.required],
    host: [null, Validators.required],
    port: [null, Validators.required],
    db: [null, Validators.required]
  });

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<CreateProjectFormComponent>,
    private resourceService: ResourceService
  ) {}

  ngOnInit() {}

  onSubmit() {
    this.resourceService.createDatabase(this.databaseForm.value);
    this.dialogRef.close();
  }
}
