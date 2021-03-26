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

@NgModule({
  declarations: [
    AppComponent,
    BrewNavbarComponent,
    ProgressComponent,
    BrewsComponent,
    SingleBrewComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule 
  ],
  providers: [BrewService],
  bootstrap: [AppComponent]
})
export class AppModule { }
