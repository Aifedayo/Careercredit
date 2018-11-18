import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Video18Component } from './video18.component';

describe('Video18Component', () => {
  let component: Video18Component;
  let fixture: ComponentFixture<Video18Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Video18Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Video18Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
