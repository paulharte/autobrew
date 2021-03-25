import { TestBed } from '@angular/core/testing';
import { AppTestModule } from '../test/app-test.module';

import { BrewService } from './brew.service';

describe('BrewService', () => {
  let service: BrewService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [AppTestModule]
    });
    service = TestBed.inject(BrewService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
