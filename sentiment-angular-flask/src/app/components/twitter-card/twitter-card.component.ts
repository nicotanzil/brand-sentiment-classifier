import {Component, Input, OnInit} from '@angular/core';
import {Tweet} from "../../models/tweet";

@Component({
  selector: 'app-twitter-card',
  templateUrl: './twitter-card.component.html',
  styleUrls: ['./twitter-card.component.scss']
})
export class TwitterCardComponent implements OnInit {

  @Input() tweet: Tweet | undefined;

  sentiment: string = "";

  constructor() { }

  ngOnInit(): void {
    if(this.tweet?.sentiment != undefined) {
      this.sentiment = this.tweet.sentiment
    }
  }
}
