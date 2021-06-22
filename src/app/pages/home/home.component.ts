import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import {faSearch} from "@fortawesome/free-solid-svg-icons";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  query: string = '';
  faSearch: any;

  constructor(
    private router: Router
  ) { }

  ngOnInit(): void {
    this.loadFontAwesome()
  }

  submitQuery(): void {
    console.log(this.query);
    this.router.navigate(['dashboard/' + this.query]).then(r => console.log(r));
  }

  submitUserQuery(): void {
    console.log(this.query)
    this.router.navigate(['user/' + this.query])
  }

  loadFontAwesome(): void {
    this.faSearch = faSearch;
  }

}
