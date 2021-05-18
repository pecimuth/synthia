import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatChipsModule } from '@angular/material/chips';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatDialogModule } from '@angular/material/dialog';
import { MatDividerModule } from '@angular/material/divider';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatMenuModule } from '@angular/material/menu';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatRadioModule } from '@angular/material/radio';
import { MatSelectModule } from '@angular/material/select';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatTableModule } from '@angular/material/table';
import { MatTabsModule } from '@angular/material/tabs';
import { AtomModule } from '../atom/atom.module';
import { DialogModule } from '../dialog/dialog.module';
import { ExportRequisitionComponent } from './export/export-requisition/export-requisition.component';
import { ExportComponent } from './export/export.component';
import { OutputChoiceComponent } from './export/output-choice/output-choice.component';
import { PreviewComponent } from './preview/preview.component';
import { TablePreviewComponent } from './preview/table-preview/table-preview.component';
import { ProjectListComponent } from './project-list/project-list.component';
import { ProjectRoutingModule } from './project-routing.module';
import { ProjectComponent } from './project.component';
import { ResourceListComponent } from './resource/resource-list/resource-list.component';
import { ResourceComponent } from './resource/resource.component';
import { ColumnFormComponent } from './table/column-form/column-form.component';
import { ConstraintListComponent } from './table/constraint-list/constraint-list.component';
import { CreateTableFormComponent } from './table/create-table-form/create-table-form.component';
import { GeneratorChoiceComponent } from './table/generator-choice/generator-choice.component';
import { GeneratorFieldComponent } from './table/generator-field/generator-field.component';
import { NullFrequencyFieldComponent } from './table/null-frequency-field/null-frequency-field.component';
import { ParamFormComponent } from './table/param-form/param-form.component';
import { TableListComponent } from './table/table-list/table-list.component';
import { TableComponent } from './table/table.component';



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
    ColumnFormComponent,
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
