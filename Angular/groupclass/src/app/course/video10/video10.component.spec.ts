import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Video10Component } from './video10.component';

describe('Video10Component', () => {
  let component: Video10Component;
  let fixture: ComponentFixture<Video10Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Video10Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Video10Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
