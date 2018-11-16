import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Video8Component } from './video8.component';

describe('Video8Component', () => {
  let component: Video8Component;
  let fixture: ComponentFixture<Video8Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Video8Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Video8Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
