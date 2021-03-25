import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from '../app-routing.module';
import { BrewNavbarComponent } from '../brew-navbar/brew-navbar.component';
import { ProgressComponent } from '../brew/progress/progress.component';
import { HttpClientTestingModule,
   } from '@angular/common/http/testing';
import { BrewService } from '../brew/brew.service';


@NgModule({
  declarations: [
    BrewNavbarComponent,
    ProgressComponent
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
