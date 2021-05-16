import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { AppTestModule } from '../../test/app-test.module';

import { ProgressComponent } from './progress.component';

describe('ProgressComponent', () => {
  let component: ProgressComponent;
  let fixture: ComponentFixture<ProgressComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProgressComponent ],
      imports: [AppTestModule]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProgressComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
  it('should create with dates', () => {
    expect(component).toBeTruthy();
    component.startTime = new Date(2021, 1, 1, 12, 0)
    component.endTime = new Date(2021, 1, 8, 12, 0)
    component.ngOnChanges({});
    fixture.detectChanges();
    expect(component).toBeTruthy();
    const completedBadge = fixture.debugElement.query(By.css('#completed-badge'));
    expect(completedBadge).toBeTruthy();
  });
});
