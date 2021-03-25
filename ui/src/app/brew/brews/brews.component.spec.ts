import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AppTestModule } from '../../test/app-test.module';

import { BrewsComponent } from './brews.component';

describe('BrewsComponent', () => {
  let component: BrewsComponent;
  let fixture: ComponentFixture<BrewsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BrewsComponent ],
      imports: [AppTestModule]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BrewsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
