import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SingleBrewComponent } from './single-brew.component';

describe('SingleBrewComponent', () => {
  let component: SingleBrewComponent;
  let fixture: ComponentFixture<SingleBrewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SingleBrewComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SingleBrewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
