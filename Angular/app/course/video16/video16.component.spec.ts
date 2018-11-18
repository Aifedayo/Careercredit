import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Video16Component } from './video16.component';

describe('Video16Component', () => {
  let component: Video16Component;
  let fixture: ComponentFixture<Video16Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Video16Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Video16Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
