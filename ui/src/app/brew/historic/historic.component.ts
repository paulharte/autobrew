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
  brewNames: string[] = [];
  requestComplete = false;

  constructor(private service: BrewService) { }

  ngOnInit(): void {
    this.service.getAllBrews().subscribe(
      brews => { 
        this.handleBrews(brews);
        this.requestComplete = true;
      }, () => this.requestComplete = true
    )
  }

  handleBrews(brews: Brew[]) {
    this.brews = [];
    for (const brew of brews) {
      if (! brew.active) {
        this.brews.push(brew)
        this.brewNames.push(brew.name)
      }
    }
  }

  onSelectBrew(event: any) {
    const brewName = event.target.value;
    if (this.brews) {
      for (const brew of this.brews) {
        if (brew.name = brewName) {
          this.selectedBrew = brew;
          return
        }

      }
    }
    
  }

}
