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
import { OverviewComponent } from './overview/overview.component';
import { TableComponent } from './table/table.component';
import { MatTabsModule } from '@angular/material/tabs';
import { TablePreviewComponent } from './table/table-preview/table-preview.component';
import { MatTableModule } from '@angular/material/table';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';


@NgModule({
  declarations: [ProjectComponent, ProjectListComponent, OverviewComponent, TableComponent, TablePreviewComponent],
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
    MatIconModule
  ]
})
export class ProjectModule { }
