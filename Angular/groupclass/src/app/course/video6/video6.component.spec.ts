import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Video6Component } from './video6.component';

describe('Video6Component', () => {
  let component: Video6Component;
  let fixture: ComponentFixture<Video6Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Video6Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Video6Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
