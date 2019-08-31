import { TestBed } from '@angular/core/testing';

import { DoorAjarService } from './door-ajar.service';

describe('DoorAjarService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: DoorAjarService = TestBed.get(DoorAjarService);
    expect(service).toBeTruthy();
  });
});
