import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { RouterModule } from '@angular/router';
import { PageHeaderComponent } from './page-header/page-header.component';
import { UserMenuComponent } from './user-menu/user-menu.component';


@NgModule({
  declarations: [
    UserMenuComponent,
    PageHeaderComponent
  ],
  imports: [
    CommonModule,
    MatMenuModule,
    MatIconModule,
    MatButtonModule,
    RouterModule,
    MatDialogModule,
    MatSnackBarModule
  ],
  exports: [
    UserMenuComponent,
    PageHeaderComponent
  ]
})
export class AtomModule { }
