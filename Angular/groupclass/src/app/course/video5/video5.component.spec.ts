import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Video5Component } from './video5.component';

describe('Video5Component', () => {
  let component: Video5Component;
  let fixture: ComponentFixture<Video5Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Video5Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Video5Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
