import { Injectable, OnDestroy } from '@angular/core';
import { GeneratorListView } from '../../api/models/generator-list-view';
import { GeneratorService } from '../../api/services';
import { BehaviorSubject, Observable } from 'rxjs';
import { GeneratorSettingView } from 'src/app/api/models/generator-setting-view';
import { GeneratorSettingWrite } from 'src/app/api/models/generator-setting-write';
import { map, tap } from 'rxjs/operators';
import { ActiveProjectService } from './active-project.service';
import { MessageView } from 'src/app/api/models/message-view';
import { GeneratorSettingCreate } from 'src/app/api/models/generator-setting-create';
import { ColumnView } from 'src/app/api/models/column-view';


export type GeneratorView = GeneratorListView['items'][0];

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

  getGeneratorByName(name: string): Observable<GeneratorView> {
    return this._generators$.pipe(
      map((generators) => {
        return generators.items
          .find((item) => item.name === name);
      })
    );
  }

  getGeneratorsForColumn(column: ColumnView): Observable<GeneratorView[]> {
    return this._generators$.pipe(
      map((generators) => {
        return generators.items.filter(
          (generator) => {
            if (!column?.col_type || !generator.only_for_type) {
              return true;
            }
            return column.col_type === generator.only_for_type;
          }
        );
      })
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

  deleteSetting(tableId: number, setting: GeneratorSettingView): Observable<MessageView> {
    return this.generatorService.deleteApiGeneratorSettingId(setting.id)
      .pipe(
        tap(() => this.activeProject.deleteGeneratorSetting(tableId, setting.id))
      );
  }

  createSetting(tableId: number,
                columnId: number,
                generator: GeneratorView): Observable<GeneratorSettingView> {
    const generatorSetting: GeneratorSettingCreate = {
      name: generator.name,
      params: {},
      null_frequency: 0,
      table_id: tableId,
      column_id: columnId
    };
    return this.generatorService.postApiGeneratorSetting(generatorSetting)
      .pipe(
        tap((createdSetting) => this.activeProject
          .addGeneratorSetting(tableId, columnId, createdSetting))
      );
  }
}
