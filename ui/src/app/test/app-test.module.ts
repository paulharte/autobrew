import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from '../app-routing.module';
import { BrewNavbarComponent } from '../brew-navbar/brew-navbar.component';
import { ProgressComponent } from '../brew/progress/progress.component';
import { HttpClientTestingModule,
   } from '@angular/common/http/testing';
import { BrewService } from '../brew/brew.service';
import { BrewsComponent } from '../brew/brews/brews.component';
import { SeriesComponent } from '../brew/measurement/series/series.component';
import { SingleBrewComponent } from '../brew/single-brew/single-brew.component';
import { StageComponent } from '../brew/stage/stage.component';
import { MeasurementsComponent } from '../brew/measurement/measurements/measurements.component';


@NgModule({
  declarations: [
    BrewNavbarComponent,
    ProgressComponent,
    BrewsComponent,
    SingleBrewComponent,
    SeriesComponent,
    StageComponent,
    MeasurementsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientTestingModule
  ],
  providers: [
    // {provide: HttpClient, useClass: httpMock}
    BrewService
  ],
  bootstrap: []
})
export class AppTestModule { }
