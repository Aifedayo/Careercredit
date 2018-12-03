import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Video11Component } from './video11.component';

describe('Video11Component', () => {
  let component: Video11Component;
  let fixture: ComponentFixture<Video11Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Video11Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Video11Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
