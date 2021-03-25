import { Component, Input, OnInit } from '@angular/core';
import { Brew } from '../brew.models';

@Component({
  selector: 'app-progress',
  templateUrl: './progress.component.html',
  styleUrls: ['./progress.component.css']
})
export class ProgressComponent implements OnInit {

  constructor() { }

  @Input() brew?: Brew;

  ngOnInit(): void {
  }

}
