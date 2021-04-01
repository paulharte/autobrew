import { Component, OnInit } from '@angular/core';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-brew-navbar',
  templateUrl: './brew-navbar.component.html',
  styleUrls: ['./brew-navbar.component.css']
})
export class BrewNavbarComponent implements OnInit {

  constructor() { }
  app_name = environment.app_name;

  ngOnInit(): void {
  }

  displayMenu(event: any) {
    console.log('click');
    const obj = document.getElementById("navbarNav");
    if (obj) {
      obj.classList.toggle("show");
    }
}

}
