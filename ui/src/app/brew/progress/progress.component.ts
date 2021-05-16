import { Component, Input, OnInit, SimpleChanges } from '@angular/core';


@Component({
  selector: 'app-progress',
  templateUrl: './progress.component.html',
  styleUrls: ['./progress.component.css']
})
export class ProgressComponent implements OnInit {

  public progress_percent = 0.0;
  public completed = false;

  constructor() { }

  @Input() startTime: Date = new Date();
  @Input() endTime: Date = new Date();

  ngOnInit(): void {
  }

  ngOnChanges(changes: SimpleChanges) {
    const total_time = this.endTime.getTime() - this.startTime.getTime();
    const time_elapsed = new Date().getTime() - this.startTime.getTime();
    this.progress_percent = this.getPercentage(total_time, time_elapsed);
    this.completed = this.progress_percent >= 100.0;
  }

  private getPercentage(total: number, current: number): number {
    const amt = current / total;
    if (amt < 0) {
      return 0.0 
    } 
    return amt * 100.0;
  }

}
