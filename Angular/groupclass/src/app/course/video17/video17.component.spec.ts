import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Video17Component } from './video17.component';

describe('Video17Component', () => {
  let component: Video17Component;
  let fixture: ComponentFixture<Video17Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Video17Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Video17Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
