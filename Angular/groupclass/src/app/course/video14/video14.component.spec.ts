import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Video14Component } from './video14.component';

describe('Video14Component', () => {
  let component: Video14Component;
  let fixture: ComponentFixture<Video14Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Video14Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Video14Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
