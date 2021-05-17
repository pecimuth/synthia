import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { DataSourceFacadeService } from 'src/app/project/service/data-source-facade.service';
import { SnackService } from 'src/app/service/snack.service';
import { ProjectFormComponent } from '../project-form/project-form.component';

@Component({
  selector: 'app-file-source-form',
  templateUrl: './file-source-form.component.html',
  styleUrls: ['./file-source-form.component.scss']
})
export class FileSourceFormComponent implements OnInit {
  @ViewChild('fileInput') fileInput!: ElementRef;

  constructor(
    private dialogRef: MatDialogRef<ProjectFormComponent>,
    private dataSourceFacade: DataSourceFacadeService,
    private snackService: SnackService
  ) {}

  ngOnInit() {}

  /**
   * Create the file data source.
   */
  submit() {
    this.dataSourceFacade.createFileSource(this.fileInput.nativeElement.files[0])
      .subscribe(
        () => this.dialogRef.close(),
        (err) => this.snackService.errorIntoSnack(err, 'Failed to upload the file')
      );
  }
}
