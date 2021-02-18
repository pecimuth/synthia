import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { ResourceService } from 'src/app/project/service/resource.service';
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
    private resourceService: ResourceService
  ) {}

  ngOnInit() {}

  onSubmit() {
    this.resourceService.createFileSource(this.fileInput.nativeElement.files[0]);
    this.dialogRef.close();
  }
}
