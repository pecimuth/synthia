import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { LandingRoutingModule } from './landing-routing.module';



@NgModule({
  declarations: [LandingPageComponent],
  imports: [
    CommonModule,
    LandingRoutingModule,
    MatButtonModule
  ]
})
export class LandingModule { }
