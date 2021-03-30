import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { BrewsComponent } from './brew/brews/brews.component';
import { HistoricComponent } from './brew/historic/historic.component';

const routes: Routes = [
  { path: 'historic', component: HistoricComponent },
  { path: '', component: BrewsComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
