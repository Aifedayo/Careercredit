import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TopicVideoComponent } from './topic-video.component';

describe('TopicVideoComponent', () => {
  let component: TopicVideoComponent;
  let fixture: ComponentFixture<TopicVideoComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TopicVideoComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TopicVideoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
