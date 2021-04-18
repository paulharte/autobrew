import { Component, OnInit } from '@angular/core';
import { Brew } from '../brew.models';
import { BrewService } from '../brew.service';

@Component({
  selector: 'app-brews',
  templateUrl: './brews.component.html',
  styleUrls: ['./brews.component.css']
})
export class BrewsComponent implements OnInit {

  activeBrews?: Brew[];
  brews?: Brew[];
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
    this.brews = brews;
    const activeOnes = [];
    for (const brew of brews) {
      if (brew.active) {
        activeOnes.push(brew);
      }
    }
    this.activeBrews = activeOnes;
  }

}
