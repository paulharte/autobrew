import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { Brew, MeasurementSeries } from './brew.models';

@Injectable({
  providedIn: 'root'
})
export class BrewService {

  BREW = 'brew';
  MEASUREMENTS = 'measurements';

  constructor(private http: HttpClient) {}

  getAllBrews(): Observable<Brew[]> {
    const url = environment.remote_url_base + this.BREW;
    return this.http.get<any[]>(url).pipe(map((brews: any[]) => brews.map((b) => new Brew(b))));
  }

  getMeasurementsForBrew(brew: Brew): Observable<MeasurementSeries[]> {
    const url = environment.remote_url_base + this.BREW + '/' +brew.remote_id + '/' + this.MEASUREMENTS;
    return this.http.get<any[]>(url).pipe(map((series: any[]) => series.map((b) => new MeasurementSeries(b))));
  }
}
