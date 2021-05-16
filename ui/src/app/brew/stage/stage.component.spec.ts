import { ComponentFixture, TestBed } from '@angular/core/testing';
import { generateTestBrew } from '../brews/brews.component.spec';

import { StageComponent } from './stage.component';

describe('StageComponent', () => {
  let component: StageComponent;
  let fixture: ComponentFixture<StageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(StageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should create with a stage', () => {
    expect(component).toBeTruthy();
    const stage = generateTestBrew().getCurrentStage();
    component.stage = stage;
    fixture.detectChanges();
    expect(component).toBeTruthy();
  });
});
