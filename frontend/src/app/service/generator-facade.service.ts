import { Injectable } from '@angular/core';
import { GeneratorListView } from '../api/models/generator-list-view';
import { GeneratorService } from '../api/services';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GeneratorFacadeService {
  private _generators$ = new BehaviorSubject<GeneratorListView>({items: []});
  get generators$() {
    return this._generators$;
  }

  constructor(
    private generatorService: GeneratorService
  ) { }

  complete() {
    this.generators$.complete();
  }

  refresh() {
    this.generatorService.getApiGenerators()
      .subscribe(
        (generators) => this._generators$.next(generators),
      );
  }
}
