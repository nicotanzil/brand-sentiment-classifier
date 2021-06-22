import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TweetGraphComponent } from './tweet-graph.component';

describe('TweetGraphComponent', () => {
  let component: TweetGraphComponent;
  let fixture: ComponentFixture<TweetGraphComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TweetGraphComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TweetGraphComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
