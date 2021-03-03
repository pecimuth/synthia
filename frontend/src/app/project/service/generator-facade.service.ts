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
export type GeneratorParam = GeneratorView['param_list'][0];

export type GeneratorsByCategory = {
  [category: string]: GeneratorView[]
};

@Injectable({
  providedIn: 'root'
})
export class GeneratorFacadeService implements OnDestroy {
  private _generators$ = new BehaviorSubject<GeneratorListView>({items: []});
  get generators$() {
    return this._generators$;
  }

  private generatorByNames$ = new BehaviorSubject<Map<string, GeneratorView>>(new Map());

  constructor(
    private generatorService: GeneratorService,
    private activeProject: ActiveProjectService
  ) { }

  ngOnDestroy() {
    this.generators$.complete();
    this.generatorByNames$.complete();
  }

  refresh() {
    this.generatorService.getApiGenerators()
      .subscribe(
        (generators) => {
          this._generators$.next(generators);
          this.refreshGeneratorsByName(generators);
        }
      );
  }

  private refreshGeneratorsByName(generatorList: GeneratorListView) {
    const map = new Map<string, GeneratorView>();
    for (const generator of generatorList.items) {
      map.set(generator.name, generator);
    }
    this.generatorByNames$.next(map);
  }

  isMultiColumn(name: string): boolean {
    const map = this.generatorByNames$.value;
    const gen = map.get(name);
    return gen && gen.is_multi_column;
  }

  getGeneratorByName(name: string): Observable<GeneratorView> {
    return this.generatorByNames$.pipe(
      map((map) => map.get(name))
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

  getGeneratorsForColumnByCategory(column: ColumnView): Observable<[GeneratorsByCategory, GeneratorView[]]> {
    return this.getGeneratorsForColumn(column).pipe(
      map((generators) => {
        const byCategory: GeneratorsByCategory = {};
        generators.forEach((generator) => {
          if (!byCategory.hasOwnProperty(generator.category)) {
            byCategory[generator.category] = [];
          }
          byCategory[generator.category].push(generator);
        });
        return [byCategory, generators];
      })
    );
  }

  static getMultiSettings(generatorSettings: GeneratorSettingView[],
                          generators: GeneratorView[]): GeneratorView[] { 
    const multiSettings = [];
    if (!generatorSettings?.length) {
      return;
    }
    const multiGenerators = new Set<string>();
    for (const generator of generators) {
      if (generator.is_multi_column) {
        multiGenerators.add(generator.name);
      }
    }
    for (const setting of generatorSettings) {
      if (multiGenerators.has(setting.name)) {
        multiSettings.push(setting);
      }
    }
    return multiSettings;
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

  patchGeneratorName(tableId: number,
                     setting: GeneratorSettingView,
                     newGenerator: GeneratorView): Observable<GeneratorSettingView> {
    const params = {
      id: setting.id,
      generatorSetting: {
        name: newGenerator.name
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
