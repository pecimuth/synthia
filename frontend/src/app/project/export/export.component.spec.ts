import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { SnackService } from 'src/app/service/snack.service';
import { Spy } from 'src/app/test';
import { ActiveProjectService } from '../service/active-project.service';
import { ExportService } from '../service/export.service';
import { HarnessLoader } from '@angular/cdk/testing';
import { TestbedHarnessEnvironment } from '@angular/cdk/testing/testbed';
import { MatButtonHarness } from '@angular/material/button/testing';
import { ExportComponent } from './export.component';

describe('ExportComponent', () => {
  let component: ExportComponent;
  let fixture: ComponentFixture<ExportComponent>;
  let loader: HarnessLoader;

  const exportServiceSpy: jasmine.SpyObj<ExportService> = jasmine.createSpyObj(
    'ExportService',
    ['export']
  );

  const activeProjectSpy = Spy.activeProjectObservableOnly();
  const snackServiceSpy = Spy.snackService();

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ExportComponent ],
      providers: [
        {provide: ActiveProjectService, useValue: activeProjectSpy},
        {provide: SnackService, useValue: snackServiceSpy},
        {provide: ExportService, useValue: exportServiceSpy}
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ExportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    loader = TestbedHarnessEnvironment.loader(fixture);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should export on click', async () => {
    exportServiceSpy.export.and.returnValue(of(null));
    const button = await loader.getHarness(MatButtonHarness);
    component.setRequisition({});
    component.setOutputChoice(null);
    expect(await button.isDisabled()).toBeFalsy();
    await button.click();
    expect(exportServiceSpy.export.calls.count()).toBe(1);
  });
});
