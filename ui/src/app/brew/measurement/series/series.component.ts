import { Component, Input, OnInit, SimpleChange } from '@angular/core';
import { ChartType } from 'angular-google-charts';
import { MeasurementSeries } from '../../brew.models';

@Component({
  selector: 'app-series',
  templateUrl: './series.component.html',
  styleUrls: ['./series.component.css']
})
export class SeriesComponent implements OnInit {

  @Input() series!: MeasurementSeries;

  public columns = ['Time', 'Measurements'];
  public chartType = ChartType.Line;
  public chartData: any[][] = [];
  public chartOptions: any = {}

  constructor() { }

  ngOnInit(): void {
    this.chartOptions = { 
      "legend": {"position": "none"}
    };
  }

  ngOnChanges(changes: SimpleChange) {
    if (this.series) {
      const out = [];
      for (const measure of this.series.measurements) {
        out.push([measure.time, measure.measurement_amt])
      }
      this.chartData = out;

      this.updateMesurementName(this.series.getDisplayName())
    }
  }

  updateMesurementName(name: string) {
    this.columns = [this.columns[0], name]
  }

}
