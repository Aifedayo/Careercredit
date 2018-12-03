import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Video12Component } from './video12.component';

describe('Video12Component', () => {
  let component: Video12Component;
  let fixture: ComponentFixture<Video12Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Video12Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Video12Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
