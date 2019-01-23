import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TopicChatComponent } from './topic-chat.component';

describe('TopicChatComponent', () => {
  let component: TopicChatComponent;
  let fixture: ComponentFixture<TopicChatComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TopicChatComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TopicChatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
