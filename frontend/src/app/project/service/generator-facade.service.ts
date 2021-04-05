import { Injectable, OnDestroy } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { ColumnView } from 'src/app/api/models/column-view';
import { GeneratorSettingCreate } from 'src/app/api/models/generator-setting-create';
import { GeneratorSettingView } from 'src/app/api/models/generator-setting-view';
import { GeneratorSettingWrite } from 'src/app/api/models/generator-setting-write';
import { MessageView } from 'src/app/api/models/message-view';
import { GeneratorListView } from '../../api/models/generator-list-view';
import { GeneratorService } from '../../api/services';
import { ActiveProjectService } from './active-project.service';


export type GeneratorView = GeneratorListView['items'][0];
export type GeneratorParam = GeneratorView['param_list'][0];

export type GeneratorsByCategory = {
  [category: string]: GeneratorView[]
};

@Injectable({
  providedIn: 'root'
})
export class GeneratorFacadeService implements OnDestroy {

  /**
   * Behavior subject of available generator types.
   */
  private _generators$ = new BehaviorSubject<GeneratorListView>({items: []});

  /**
   * Get behavior subject of available generator types.
   */
  get generators$() {
    return this._generators$;
  }

  /**
   * Behavior subject of available generator types mapped by name.
   */
  private generatorByNames$ = new BehaviorSubject<Map<string, GeneratorView>>(new Map());

  constructor(
    private generatorService: GeneratorService,
    private activeProject: ActiveProjectService
  ) { }

  ngOnDestroy() {
    this.generators$.complete();
    this.generatorByNames$.complete();
  }

  /**
   * Fetch available generator types from the API.
   */
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

  /**
   * Return whether a generator is suited for multiple columns.
   * 
   * @param name - Name of the generator
   * @returns Is the generator multi column?
   */
  isMultiColumn(name: string): boolean {
    const map = this.generatorByNames$.value;
    const gen = map.get(name);
    return gen && gen.is_multi_column;
  }

  /**
   * Return generator type by name.
   * 
   * @param name - Name of the generator
   * @returns Observable of generator type
   */
  getGeneratorByName(name: string): Observable<GeneratorView> {
    return this.generatorByNames$.pipe(
      map((map) => map.get(name))
    );
  }

  /**
   * Return the list of suitable generators for a column.
   * 
   * @param column - The column
   * @returns Observable of the list of suitable generators
   */
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

  /**
   * Return the list of suitable generator for a column and also mapped by category.
   * 
   * @param column - The column
   * @returns Observable of the mapping of suitable generators by category and a flat list
   * of suitable generators
   */
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

  /**
   * From a list generator settings and generator types,
   * return list of multi-column generator settings.
   * 
   * @param generatorSettings - The list of generator settings
   * @param generators - The list of available generator types
   * @returns List of multi-column generators
   */
  static getMultiSettings(generatorSettings: GeneratorSettingView[],
                          generators: GeneratorView[]): GeneratorSettingView[] { 
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

  /**
   * Patch a generator setting via the API and update the active project state.
   * 
   * @param tableId - The ID of the table containing the generator setting
   * @param settingId - The ID of the setting to be patched
   * @param setting - The setting patch
   * @returns Observable of the patched setting
   */
  patchParams(tableId: number,
              settingId: number,
              setting: GeneratorSettingWrite): Observable<GeneratorSettingView> {
    const params = {
      id: settingId,
      generatorSetting: setting
    };
    return this.generatorService.patchApiGeneratorSettingId(params)
      .pipe(
        tap(
          (patchedSetting) => this.activeProject
            .patchGeneratorSetting(tableId, patchedSetting)
        )
      );
  }

  /**
   * Change generator setting's generator name via the API and update the active project
   * state.
   * 
   * @param tableId - The ID of the table containing the generator setting
   * @param settingId - The ID of the setting to be patched
   * @param generator - The new generator
   * @returns Observable of the patched setting
   */
  patchGeneratorName(tableId: number,
                     settingId: number,
                     generator: GeneratorView): Observable<GeneratorSettingView> {
    const params = {
      id: settingId,
      generatorSetting: {
        name: generator.name
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

  /**
   * Delete a generator setting via the API and update the active project state.
   * 
   * @param tableId - The ID of the table containing the setting
   * @param settingId - The ID of the setting to be deleted
   * @returns Observable of the operation status message
   */
  deleteSetting(tableId: number, settingId: number): Observable<MessageView> {
    return this.generatorService.deleteApiGeneratorSettingId(settingId)
      .pipe(
        tap(() => this.activeProject.deleteGeneratorSetting(tableId, settingId))
      );
  }

  /**
   * Create a new generator setting and assign it to a column via the API;
   * update the active project state.
   * 
   * @param tableId - The ID of the table containing the new setting
   * @param columnId - The ID of the assigned column
   * @param generator - The new generator
   * @returns Obserable of the created generator setting.
   */
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
