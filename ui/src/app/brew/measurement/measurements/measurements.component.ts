import { Component, Input, OnInit, SimpleChange } from '@angular/core';
import { Brew, MeasurementSeries } from '../../brew.models';
import { BrewService } from '../../brew.service';

@Component({
  selector: 'app-measurements',
  templateUrl: './measurements.component.html',
  styleUrls: ['./measurements.component.css']
})
export class MeasurementsComponent implements OnInit {

  @Input() brew?: Brew;

  measurementSeries:MeasurementSeries[] = []
  requestComplete = false;

  constructor(private brewService: BrewService) { }

  ngOnInit(): void {
  }

  ngOnChanges(changes: SimpleChange) {
    if(this.brew) {
      this.brewService.getMeasurementsForBrew(this.brew).subscribe(
        series =>  {
          this.measurementSeries = series;
          this.requestComplete = true;
        }, () => this.requestComplete = true
      )
    }
    
  }


}
