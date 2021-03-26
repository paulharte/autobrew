import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AppTestModule } from 'src/app/test/app-test.module';

import { MeasurementsComponent } from './measurements.component';

describe('MeasurementsComponent', () => {
  let component: MeasurementsComponent;
  let fixture: ComponentFixture<MeasurementsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MeasurementsComponent ],
      imports: [AppTestModule]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MeasurementsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
