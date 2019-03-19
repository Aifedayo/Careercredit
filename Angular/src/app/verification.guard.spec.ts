import { TestBed, async, inject } from '@angular/core/testing';

import { VerificationGuard } from './verification.guard';

describe('VerificationGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [VerificationGuard]
    });
  });

  it('should ...', inject([VerificationGuard], (guard: VerificationGuard) => {
    expect(guard).toBeTruthy();
  }));
});
