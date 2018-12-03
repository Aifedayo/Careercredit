import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Video7Component } from './video7.component';

describe('Video7Component', () => {
  let component: Video7Component;
  let fixture: ComponentFixture<Video7Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Video7Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Video7Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
