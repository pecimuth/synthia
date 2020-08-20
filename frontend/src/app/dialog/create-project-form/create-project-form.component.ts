import { Component, OnInit } from '@angular/core';
import { ProjectService } from 'src/app/api/services';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, Validators, FormControl } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';

const snackConfig = {
  duration: 2000
};

@Component({
  selector: 'app-create-project-form',
  templateUrl: './create-project-form.component.html',
  styleUrls: ['./create-project-form.component.scss']
})
export class CreateProjectFormComponent implements OnInit {
  projectForm = this.fb.group({
    engine: [{value: 'SQLite', disabled: true}, Validators.required],
    name: [null, Validators.required]
  });

  constructor(
    private fb: FormBuilder,
    private projectService: ProjectService,
    private projectFacade: ProjectFacadeService,
    private dialogRef: MatDialogRef<CreateProjectFormComponent>,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit() {}

  onSubmit() {
    this.projectService
      .postApiProject(this.projectForm.value['name'])
      .subscribe(
        (project) => {
          this.snackBar.open(`Created project ${project.name}`, 'OK', snackConfig);
          this.projectFacade.refreshList();
          this.dialogRef.close()
        },
        () => {
          this.snackBar.open('Could not create a project', 'OK', snackConfig);
        }
      );
  }
}
