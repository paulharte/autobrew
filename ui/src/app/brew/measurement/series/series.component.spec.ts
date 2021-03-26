import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MeasurementSeries } from '../../brew.models';

import { SeriesComponent } from './series.component';

describe('SeriesComponent', () => {
  let component: SeriesComponent;
  let fixture: ComponentFixture<SeriesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SeriesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SeriesComponent);
    component = fixture.componentInstance;
    
  });

  it('should create', () => {
    component.series = new MeasurementSeries({"source_name": "temperature1",
    "brew_id": "1",
    "brew_remote_id": "asdfasd123",
    "measurements": [],})
    fixture.detectChanges();
    expect(component).toBeTruthy();
  });
});
