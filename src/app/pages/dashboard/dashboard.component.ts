import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {Tweet} from "../../models/tweet";
import {AppService} from "../../services/app.service";

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  tweets: Tweet[] = [];
  keyword: string = '';
  pos_count: number = 0;
  neg_count: number = 0;

  constructor(
    private actRoute: ActivatedRoute,
    private appService: AppService
  ) {}

  ngOnInit(): void {
    this.keyword = this.actRoute.snapshot.params.keyword;
    console.log('finding ' + this.keyword);
    this.appService.getByKeyword(this.keyword).subscribe(query => {
      this.tweets = query.data;
      console.log(this.tweets)
      this.tweets.forEach(tweet => {
        if(tweet.sentiment == "Positive") this.pos_count++;
        else this.neg_count++;
      })
    }, error => {
      console.log(error)
    })
  }

}
