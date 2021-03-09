import { Component, OnInit } from '@angular/core';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { MatDialogRef } from '@angular/material/dialog';
import { FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Snack } from 'src/app/service/constants';
import { Router } from '@angular/router';
@Component({
  selector: 'app-create-project-form',
  templateUrl: './create-project-form.component.html',
  styleUrls: ['./create-project-form.component.scss']
})
export class CreateProjectFormComponent implements OnInit {
  projectForm = this.fb.group({
    name: [null, Validators.required]
  });

  constructor(
    private fb: FormBuilder,
    private projectFacade: ProjectFacadeService,
    private dialogRef: MatDialogRef<CreateProjectFormComponent>,
    private snackBar: MatSnackBar,
    private router: Router
  ) {}

  ngOnInit() {}

  submit() {
    if (!this.projectForm.valid) {
      return;
    }
    this.projectFacade
      .createProject(this.projectForm.value['name'])
      .subscribe(
        (project) => {
          this.snackBar.open(`Created project ${project.name}`, Snack.OK, Snack.CONFIG);
          this.dialogRef.close();
          this.router.navigate(['project', project.id]);
        },
        () => {
          this.snackBar.open('Could not create a project', Snack.OK, Snack.CONFIG);
        }
      );
  }
}
