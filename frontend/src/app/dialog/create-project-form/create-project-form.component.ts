import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { SnackService } from 'src/app/service/snack.service';

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
    private router: Router,
    private snackService: SnackService
  ) {}

  ngOnInit() {}

  /**
   * Create the project.
   */
  submit() {
    if (!this.projectForm.valid) {
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
