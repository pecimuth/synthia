import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { switchMap } from 'rxjs/operators';
import { AuthFacadeService } from 'src/app/service/auth-facade.service';
import { Snack } from 'src/app/service/constants';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.scss']
})
export class LandingPageComponent implements OnInit {

  constructor(
    private authFacade: AuthFacadeService,
    private projectFacade: ProjectFacadeService,
    private snackBar: MatSnackBar,
    private router: Router
  ) { }

  ngOnInit(): void {
  }

  startNow() {
    if (this.authFacade.isLoggedIn) {
      return;
    }
    this.authFacade.register(null, null)
      .pipe(
        switchMap(() => this.projectFacade.createProject('My Project 1')),
      )
      .subscribe(
        (project) => {
          this.snackBar.open('Created a project', Snack.OK, Snack.CONFIG);
          this.router.navigate(['/project', project.id]);
        },
        () => {
          this.snackBar.open('Could not start a project', Snack.OK, Snack.CONFIG);
        }
      );
  }
}
