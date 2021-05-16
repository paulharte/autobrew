import { Component, Input, OnInit } from '@angular/core';
import { Brew } from '../brew.models';

@Component({
  selector: 'app-single-brew',
  templateUrl: './single-brew.component.html',
  styleUrls: ['./single-brew.component.css']
})
export class SingleBrewComponent implements OnInit {


  @Input() brew!: Brew;

  constructor() { }

  ngOnInit(): void {
  }

}
