import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ProjectRoutingModule } from './project-routing.module';
import { ProjectComponent } from './project.component';
import { ProjectListComponent } from './project-list/project-list.component';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { AtomModule } from '../atom/atom.module';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { TableComponent } from './table/table.component';
import { MatTabsModule } from '@angular/material/tabs';
import { TablePreviewComponent } from './preview/table-preview/table-preview.component';
import { MatTableModule } from '@angular/material/table';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { ParamFormComponent } from './table/param-form/param-form.component';
import { ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatDividerModule } from '@angular/material/divider';
import { MatSelectModule } from '@angular/material/select';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatExpansionModule } from '@angular/material/expansion';
import { TableListComponent } from './table/table-list/table-list.component';
import { ResourceListComponent } from './resource/resource-list/resource-list.component';
import { PreviewComponent } from './preview/preview.component';
import { ExportComponent } from './export/export.component';
import { ResourceComponent } from './resource/resource.component';
import { TableCountComponent } from './export/table-count/table-count.component';
import { OutputChoiceComponent } from './export/output-choice/output-choice.component';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatRadioModule } from '@angular/material/radio';
import { MatDialogModule } from '@angular/material/dialog';
import { GeneratorChoiceComponent } from './table/generator-choice/generator-choice.component';


@NgModule({
  declarations: [
    ProjectComponent,
    ProjectListComponent,
    TableComponent,
    TablePreviewComponent,
    ParamFormComponent,
    TableListComponent,
    ResourceListComponent,
    PreviewComponent,
    ExportComponent,
    ResourceComponent,
    TableCountComponent,
    OutputChoiceComponent,
    GeneratorChoiceComponent
  ],
  imports: [
    CommonModule,
    ProjectRoutingModule,
    MatCardModule,
    MatButtonModule,
    AtomModule,
    MatSidenavModule,
    MatListModule,
    MatTabsModule,
    MatTableModule,
    MatChipsModule,
    MatIconModule,
    ReactiveFormsModule,
    MatInputModule,
    MatDividerModule,
    MatSelectModule,
    MatSnackBarModule,
    MatExpansionModule,
    MatCheckboxModule,
    MatRadioModule,
    MatDialogModule,
    MatButtonModule
  ]
})
export class ProjectModule { }
