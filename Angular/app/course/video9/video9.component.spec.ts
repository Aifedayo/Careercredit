import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Video9Component } from './video9.component';

describe('Video9Component', () => {
  let component: Video9Component;
  let fixture: ComponentFixture<Video9Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Video9Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Video9Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
