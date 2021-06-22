import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {Tweet} from "../../models/tweet";
import {AppService} from "../../services/app.service";
import {TweetGraph} from "../../models/tweet-graph";
import {Hashtag} from "../../models/hashtag";

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  tweets: Tweet[] = [];
  recent_tweets: Tweet[] = [];
  tweet_graphs: TweetGraph[] = [];
  hashtags: string[] = [];
  keyword: string = '';
  search_keyword: string = '';
  pos_count: number = 0;
  neg_count: number = 0;

  pos_count_recent: number = 0;
  neg_count_recent: number = 0;

  isLoading: boolean = true;

  constructor(
    private actRoute: ActivatedRoute,
    private appService: AppService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.keyword = this.actRoute.snapshot.params.keyword;
    console.log('finding ' + this.keyword);
    if(this.keyword.startsWith("#")) this.search_keyword = this.formatRequest(this.keyword);
    else this.search_keyword = this.keyword;
    this.appService.getByKeyword(this.search_keyword).subscribe(query => {
      this.tweets = query.data;
      this.recent_tweets = query.recent_data;
      this.tweet_graphs = query.graph_data;
      this.getAllHashtags();
      this.tweets.forEach(tweet => {
        if(tweet.sentiment == "Positive") this.pos_count++;
        else this.neg_count++;
      })
      this.recent_tweets.forEach(tweet => {
        if(tweet.sentiment == "Positive") this.pos_count_recent++;
        else this.neg_count_recent++;
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

  formatRequest(request: string) {
    const re = /#/gi;
    return request.replace(re, "%23") + " ";
  }

}
