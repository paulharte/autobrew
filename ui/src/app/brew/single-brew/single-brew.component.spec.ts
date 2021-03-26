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

  it('should cal end date', () => {
    const start = new Date(2020, 11, 1, 18, 0);
    const end = component.getEndTime(start);
    expect(end.getDate()).toEqual(8);
    expect(end.getFullYear()).toEqual(2020);
    expect(end.getHours()).toEqual(18);

    const start2 = new Date(2020, 6, 31, 18, 0);
    const end2 = component.getEndTime(start2);
    expect(end2.getDate()).toEqual(7);
    expect(end2.getFullYear()).toEqual(2020);
    expect(end2.getHours()).toEqual(18);
    expect(end2.getMonth()).toEqual(7);

  });
});
