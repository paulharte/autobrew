import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BrewNavbarComponent } from './brew-navbar.component';

describe('BrewNavbarComponent', () => {
  let component: BrewNavbarComponent;
  let fixture: ComponentFixture<BrewNavbarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BrewNavbarComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BrewNavbarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
