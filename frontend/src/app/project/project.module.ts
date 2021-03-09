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
import { OutputChoiceComponent } from './export/output-choice/output-choice.component';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatRadioModule } from '@angular/material/radio';
import { MatDialogModule } from '@angular/material/dialog';
import { GeneratorChoiceComponent } from './table/generator-choice/generator-choice.component';
import { ConstraintListComponent } from './table/constraint-list/constraint-list.component';
import { NullFrequencyFieldComponent } from './table/null-frequency-field/null-frequency-field.component';
import { MatMenuModule } from '@angular/material/menu';
import { CreateColumnFormComponent } from './table/create-column-form/create-column-form.component';
import { MatFormFieldModule } from '@angular/material/form-field';
import { DialogModule } from '../dialog/dialog.module';
import { CreateTableFormComponent } from './table/create-table-form/create-table-form.component';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { GeneratorFieldComponent } from './table/generator-field/generator-field.component';
import { ExportRequisitionComponent } from './export/export-requisition/export-requisition.component';
import { MatProgressBarModule } from '@angular/material/progress-bar';


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
    OutputChoiceComponent,
    GeneratorChoiceComponent,
    ConstraintListComponent,
    NullFrequencyFieldComponent,
    CreateColumnFormComponent,
    CreateTableFormComponent,
    GeneratorFieldComponent,
    ExportRequisitionComponent
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
    MatButtonModule,
    MatMenuModule,
    MatFormFieldModule,
    DialogModule,
    MatDatepickerModule,
    MatProgressBarModule
  ]
})
export class ProjectModule { }
