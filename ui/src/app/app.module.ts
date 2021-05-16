import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrewNavbarComponent } from './brew-navbar/brew-navbar.component';
import { ProgressComponent } from './brew/progress/progress.component';
import { BrewsComponent } from './brew/brews/brews.component';
import { BrewService } from './brew/brew.service';
import { SingleBrewComponent } from './brew/single-brew/single-brew.component';
import { SeriesComponent } from './brew/measurement/series/series.component';
import { GoogleChartsModule } from 'angular-google-charts';
import { MeasurementsComponent } from './brew/measurement/measurements/measurements.component';
import { HistoricComponent } from './brew/historic/historic.component';
import { StageComponent } from './brew/stage/stage.component';

@NgModule({
  declarations: [
    AppComponent,
    BrewNavbarComponent,
    ProgressComponent,
    BrewsComponent,
    SingleBrewComponent,
    SeriesComponent,
    MeasurementsComponent,
    HistoricComponent,
    StageComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    GoogleChartsModule 
  ],
  providers: [BrewService],
  bootstrap: [AppComponent]
})
export class AppModule { }
