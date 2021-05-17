import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { ProjectView } from 'src/app/api/models';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { SnackService } from 'src/app/service/snack.service';

@Component({
  selector: 'app-project-form',
  templateUrl: './project-form.component.html',
  styleUrls: ['./project-form.component.scss']
})
export class ProjectFormComponent implements OnInit {
  projectForm = this.fb.group({
    name: [null, Validators.required]
  });

  constructor(
    private fb: FormBuilder,
    private projectFacade: ProjectFacadeService,
    private dialogRef: MatDialogRef<ProjectFormComponent>,
    private router: Router,
    private snackService: SnackService,
    @Inject(MAT_DIALOG_DATA) public project: ProjectView
  ) {}

  ngOnInit() {
    if (this.project) {
      this.projectForm.controls.name.setValue(this.project.name);
    }
  }

  /**
   * Rename a project in case a project instance was passed to the constructor.
   * Otherwise create a new project and navigate to it.
   */
  submit() {
    if (!this.projectForm.valid) {
      return;
    }

    if (this.project) {
      this.projectFacade
        .renameProject(this.project.id, this.projectForm.value['name'])
        .subscribe(
          (newProject) => {
            this.snackService.snack(`Renamed the project to ${newProject.name}`);
            this.dialogRef.close();
          },
        () => {
          this.snackService.snack('Could not rename the project');
        });
      return;
    }

    this.projectFacade
      .createProject(this.projectForm.value['name'])
      .subscribe(
        (project) => {
          this.snackService.snack(`Created project ${project.name}`);
          this.dialogRef.close();
          this.router.navigate(['project', project.id]);
        },
        () => {
          this.snackService.snack('Could not create a project');
        }
      );
  }
}
