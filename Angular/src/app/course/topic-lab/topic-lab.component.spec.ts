import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TopicLabComponent } from './topic-lab.component';

describe('TopicLabComponent', () => {
  let component: TopicLabComponent;
  let fixture: ComponentFixture<TopicLabComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TopicLabComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TopicLabComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
