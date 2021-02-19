import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ProjectComponent } from './project.component';
import { ProjectListComponent } from './project-list/project-list.component';
import { TableListComponent } from './table/table-list/table-list.component';
import { ResourceListComponent } from './resource/resource-list/resource-list.component';
import { PreviewComponent } from './preview/preview.component';
import { ExportComponent } from './export/export.component';

const routes: Routes = [
  {
    path: ':id',
    component: ProjectComponent,
    children: [
      {
        path: 'resources',
        component: ResourceListComponent
      },
      {
        path: 'tables',
        component: TableListComponent
      },
      {
        path: 'preview',
        component: PreviewComponent
      },
      {
        path: 'export',
        component: ExportComponent
      },
      {
        path: '',
        redirectTo: 'resources',
        pathMatch: 'full'
      },
    ]
  },
  {
    path: '',
    component: ProjectListComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProjectRoutingModule { }
