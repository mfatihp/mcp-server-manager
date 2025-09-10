import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LlmchatComponent } from './llmchat.component';

describe('LlmchatComponent', () => {
  let component: LlmchatComponent;
  let fixture: ComponentFixture<LlmchatComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LlmchatComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LlmchatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
