import { Component, Input, OnInit } from '@angular/core';
import { Brew } from '../brew.models';

@Component({
  selector: 'app-single-brew',
  templateUrl: './single-brew.component.html',
  styleUrls: ['./single-brew.component.css']
})
export class SingleBrewComponent implements OnInit {

  DAYS_TO_BREW = 7;

  @Input() brew!: Brew;

  constructor() { }

  ngOnInit(): void {
  }

  getEndTime(startTime: Date): Date {

    var date = new Date(startTime.valueOf());
    date.setDate(date.getDate() + this.DAYS_TO_BREW);
    return date;
  }

}
