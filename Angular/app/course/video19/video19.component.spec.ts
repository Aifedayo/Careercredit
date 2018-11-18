import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Video19Component } from './video19.component';

describe('Video19Component', () => {
  let component: Video19Component;
  let fixture: ComponentFixture<Video19Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Video19Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Video19Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
