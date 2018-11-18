import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Video15Component } from './video15.component';

describe('Video15Component', () => {
  let component: Video15Component;
  let fixture: ComponentFixture<Video15Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Video15Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Video15Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
