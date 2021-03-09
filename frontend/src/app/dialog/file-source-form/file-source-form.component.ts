import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { DataSourceFacadeService } from 'src/app/project/service/data-source-facade.service';
import { SnackService } from 'src/app/service/snack.service';
import { CreateProjectFormComponent } from '../create-project-form/create-project-form.component';

@Component({
  selector: 'app-file-source-form',
  templateUrl: './file-source-form.component.html',
  styleUrls: ['./file-source-form.component.scss']
})
export class FileSourceFormComponent implements OnInit {
  @ViewChild('fileInput') fileInput!: ElementRef;

  constructor(
    private dialogRef: MatDialogRef<CreateProjectFormComponent>,
    private dataSourceFacade: DataSourceFacadeService,
    private snackService: SnackService
  ) {}

  ngOnInit() {}

  submit() {
    this.dataSourceFacade.createFileSource(this.fileInput.nativeElement.files[0])
      .subscribe(
        () => this.dialogRef.close(),
        (err) => this.snackService.errorIntoSnack(err, 'Failed to upload the file')
      );
  }
}
