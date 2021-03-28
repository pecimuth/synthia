import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { switchMap } from 'rxjs/operators';
import { AuthFacadeService } from 'src/app/service/auth-facade.service';
import { ProjectFacadeService } from 'src/app/service/project-facade.service';
import { SnackService } from 'src/app/service/snack.service';

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.scss']
})
export class LandingPageComponent implements OnInit {

  constructor(
    private authFacade: AuthFacadeService,
    private projectFacade: ProjectFacadeService,
    private snackService: SnackService,
    private router: Router
  ) { }

  ngOnInit(): void {
  }

  /**
   * Create an anonymous account and start a new project.
   * No effect for a loggen in user.
   */
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
          this.snackService.snack('Created a project');
          this.router.navigate(['/project', project.id]);
        },
        () => {
          this.snackService.snack('Could not start a project');
        }
      );
  }
}
