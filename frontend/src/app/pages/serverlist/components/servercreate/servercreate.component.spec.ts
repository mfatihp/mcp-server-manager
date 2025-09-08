import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ServercreateComponent } from './servercreate.component';

describe('ServercreateComponent', () => {
  let component: ServercreateComponent;
  let fixture: ComponentFixture<ServercreateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ServercreateComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ServercreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
