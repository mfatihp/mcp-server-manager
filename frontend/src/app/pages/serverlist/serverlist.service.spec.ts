import { TestBed } from '@angular/core/testing';

import { ServerlistService } from './serverlist.service';

describe('ServerlistService', () => {
  let service: ServerlistService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ServerlistService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
