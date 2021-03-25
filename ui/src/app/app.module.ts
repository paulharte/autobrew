import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrewNavbarComponent } from './brew-navbar/brew-navbar.component';
import { ProgressComponent } from './brew/progress/progress.component';

@NgModule({
  declarations: [
    AppComponent,
    BrewNavbarComponent,
    ProgressComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule 
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
