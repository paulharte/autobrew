import { Component, Input, OnInit } from '@angular/core';
import { ChartType } from 'angular-google-charts';
import { MeasurementSeries } from '../../brew.models';

@Component({
  selector: 'app-series',
  templateUrl: './series.component.html',
  styleUrls: ['./series.component.css']
})
export class SeriesComponent implements OnInit {

  @Input() series!: MeasurementSeries;

  public chartType = ChartType.Line;
  public chartData = [];

  constructor() { }

  ngOnInit(): void {
  }

}
