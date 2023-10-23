import { Component, OnInit } from '@angular/core';
import { Brew } from '../brew.models';
import { BrewService } from '../brew.service';

@Component({
  selector: 'app-historic',
  templateUrl: './historic.component.html',
  styleUrls: ['./historic.component.css']
})
export class HistoricComponent implements OnInit {

  selectedBrew?: Brew;
  brews?: Brew[];
  brewNames?: string[];
  requestComplete = false;

  constructor(private service: BrewService) { }

  ngOnInit(): void {
    this.service.getAllBrews().subscribe(
      incomingBrews => {
        this.handleBrews(incomingBrews);
        this.requestComplete = true;
      }, () => this.requestComplete = true
    );
  }

  handleBrews(incomingBrews: Brew[]): void {
    const inactiveBrews = [];
    const names = [];
    for (const brew of incomingBrews) {
      if (brew.isComplete()) {
        inactiveBrews.push(brew);
        names.push(brew.name);
      }
    }
    this.brews = inactiveBrews;
    this.brewNames = names;
  }

  onSelectBrew(event: any): void {
    const brewName = event.target.value;
    if (this.brews) {
      for (const brew of this.brews) {
        if (brew.name === brewName) {
          this.selectedBrew = brew;
          return;
        }
      }
    }
  }

}
