import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AppTestModule } from '../../test/app-test.module';
import { Brew } from '../brew.models';

import { BrewsComponent } from './brews.component';

describe('BrewsComponent', () => {
  let component: BrewsComponent;
  let fixture: ComponentFixture<BrewsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BrewsComponent ],
      imports: [AppTestModule]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BrewsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should create with a brew', () => {
    expect(component).toBeTruthy();
    const brews = [generateTestBrew()];
    component.handleBrews(brews);
    component.requestComplete = true;
    expect(component.activeBrews).toEqual(brews);
    fixture.detectChanges();
    expect(component).toBeTruthy();
  });
});


export function generateTestBrew(): Brew {

  const TEST_FERMENT_STAGE = [{"start_time": "2021-05-15T19:30:54.100000", "stage_name": "FERMENTING",
                       "estimated_end_time": "2021-05-22T19:30:54.100000"}]

  const j ={
    "name": "brew1",
    "id": "1",
    "remote_id": "remote_id",
    "active": true,
    "start_time": "2021-05-15T19:30:54.100000",
    "stages": TEST_FERMENT_STAGE,
  }
  return new Brew(j);

}