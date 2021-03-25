import { TestBed } from '@angular/core/testing';

import { BrewService } from './brew.service';

describe('BrewService', () => {
  let service: BrewService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BrewService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
