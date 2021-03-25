import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class BrewService {

  BREW = 'brew';
  MEASUREMENTS = 'measurements';

  constructor(private http: HttpClient) {}

  getAllBrews(): Observable<Brew[]> {
    const url = environment.remote_url_base + this.BREW;
    return this.http.get<Brew[]>(url)
  }

  getMeasurementsForBrew(brew: Brew): Observable<MeasurementSeries[]> {
    const url = environment.remote_url_base + this.BREW + '/' +brew.remote_id + '/' + this.MEASUREMENTS;
    return this.http.get<MeasurementSeries[]>(url)
  }
}
