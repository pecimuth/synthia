import { Injectable, OnDestroy } from '@angular/core';
import { GeneratorListView } from '../../api/models/generator-list-view';
import { GeneratorService } from '../../api/services';
import { BehaviorSubject, Observable } from 'rxjs';
import { GeneratorSettingView } from 'src/app/api/models/generator-setting-view';
import { GeneratorSettingWrite } from 'src/app/api/models/generator-setting-write';
import { tap } from 'rxjs/operators';
import { ActiveProjectService } from './active-project.service';

@Injectable({
  providedIn: 'root'
})
export class GeneratorFacadeService implements OnDestroy {
  private _generators$ = new BehaviorSubject<GeneratorListView>({items: []});
  get generators$() {
    return this._generators$;
  }

  constructor(
    private generatorService: GeneratorService,
    private activeProject: ActiveProjectService
  ) { }

  ngOnDestroy() {
    this.generators$.complete();
  }

  refresh() {
    this.generatorService.getApiGenerators()
      .subscribe(
        (generators) => this._generators$.next(generators),
      );
  }

  patchParams(tableId: number,
              setting: GeneratorSettingView,
              newSetting: GeneratorSettingWrite): Observable<GeneratorSettingView> {
    const params = {
      id: setting.id,
      generatorSetting: {
        ...{
          name: setting.name,
          params: setting.params
        },
        ...newSetting
      }
    };
    return this.generatorService.patchApiGeneratorSettingId(params)
      .pipe(
        tap(
          (patchedSetting) => this.activeProject
            .patchGeneratorSetting(tableId, patchedSetting)
        )
      );
  }
}
