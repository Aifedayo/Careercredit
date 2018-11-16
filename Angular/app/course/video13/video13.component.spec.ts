import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Video13Component } from './video13.component';

describe('Video13Component', () => {
  let component: Video13Component;
  let fixture: ComponentFixture<Video13Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Video13Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Video13Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
