import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Video3Component } from './video3.component';

describe('Video3Component', () => {
  let component: Video3Component;
  let fixture: ComponentFixture<Video3Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Video3Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Video3Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
