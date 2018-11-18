import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Video4Component } from './video4.component';

describe('Video4Component', () => {
  let component: Video4Component;
  let fixture: ComponentFixture<Video4Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Video4Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Video4Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
