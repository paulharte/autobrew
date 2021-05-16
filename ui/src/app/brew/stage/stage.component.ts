import { Component, Input, OnInit } from '@angular/core';
import { Stage } from '../brew.models';

@Component({
  selector: 'app-stage',
  templateUrl: './stage.component.html',
  styleUrls: ['./stage.component.css']
})
export class StageComponent implements OnInit {

  @Input() stage!: Stage;

  constructor() { }

  ngOnInit(): void {
  }

}
