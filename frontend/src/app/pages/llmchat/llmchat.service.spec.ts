import { TestBed } from '@angular/core/testing';

import { LlmchatService } from './llmchat.service';

describe('LlmchatService', () => {
  let service: LlmchatService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LlmchatService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
