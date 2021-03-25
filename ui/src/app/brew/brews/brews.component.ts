import { Component, OnInit } from '@angular/core';
import { Brew } from '../brew.models';
import { BrewService } from '../brew.service';

@Component({
  selector: 'app-brews',
  templateUrl: './brews.component.html',
  styleUrls: ['./brews.component.css']
})
export class BrewsComponent implements OnInit {

  activeBrew?: Brew;
  brews?: Brew[];
  constructor(private service: BrewService) { }

  ngOnInit(): void {
    this.service.getAllBrews().subscribe(
      brews => this.handleBrews(brews)
    )
  }

  handleBrews(brews: Brew[]) {
    this.brews = brews;
    for (const brew of brews) {
      if (brew.active) {
        this.activeBrew = brew;
      }
    }
  }

}
