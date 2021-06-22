import { Component, OnInit } from '@angular/core';
import {Tweet} from "../../models/tweet";
import {TweetGraph} from "../../models/tweet-graph";
import {ActivatedRoute, Router} from "@angular/router";
import {AppService} from "../../services/app.service";

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.scss']
})
export class UserProfileComponent implements OnInit {

  tweets: Tweet[] = [];
  keyword: string = '';
  hashtags: string[] = [];
  pos_count: number = 0;
  neg_count: number = 0;

  first_tweet!: Tweet;

  isLoading: boolean = true;

  constructor(
    private actRoute: ActivatedRoute,
    private appService: AppService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.keyword = this.actRoute.snapshot.params.keyword;
    this.appService.getByUser(this.keyword).subscribe(query => {
      this.tweets = query.data;
      this.getAllHashtags();
      this.first_tweet = this.tweets[0]
      this.tweets.forEach(tweet => {
        if(tweet.sentiment == "Positive") this.pos_count++;
        else this.neg_count++;
      })
      this.isLoading = false;
    }, error => {
      console.log(error)
    })
  }

  getAllHashtags() {
    this.tweets.forEach(tweet => {
      tweet.entities.hashtags.forEach(hashtag => {
        if(!this.isExists(hashtag.text)) {
          this.hashtags.push(hashtag.text);
        }
      })
    });
  }

  isExists(text: string) {
    let x = false;
    this.hashtags.forEach(hashtag => {
      if(hashtag == text) x = true;
    });
    return x;
  }

  redirectHashtag(hashtag: string) {
    window.open('dashboard/#' + hashtag, "_blank")
  }
}
