import {Component, Input, OnChanges, OnInit, SimpleChanges} from '@angular/core';
import {TweetGraph} from "../../models/tweet-graph";
import {ChartDataSets, ChartOptions, ChartType} from "chart.js";
import {Label} from "ng2-charts";

@Component({
  selector: 'app-tweet-graph',
  templateUrl: './tweet-graph.component.html',
  styleUrls: ['./tweet-graph.component.scss']
})
export class TweetGraphComponent implements OnInit, OnChanges {

  @Input() graphDatas: TweetGraph[] | undefined;

  dates: any[];
  pos_count: number[];
  neg_count: number[];

  lineChartData: ChartDataSets[] = [];
  lineChartLabels: Label[] = [];
  lineChartOptions!: (ChartOptions & { annonation: any });
  lineChartLegend!: boolean;
  lineChartType!: ChartType;

  graphReady: boolean;

  constructor() {
    this.graphDatas = [];
    this.dates = [];
    this.pos_count = [];
    this.neg_count = [];

    this.graphReady = false;
  }

  preprocessData(): void {
    this.graphDatas?.forEach(data => {
      console.log("Preprocess data")
      console.log(data)
      this.pos_count.push(data.pos_count)
      this.neg_count.push(data.neg_count)
      this.dates.push(data.date.substring(0, 10))
    });
  }

  initGraph(): void {
    this.preprocessData();
    console.log(this.pos_count)
    console.log(this.neg_count)
    console.log(this.dates)
    this.lineChartData = [
      { data: this.neg_count, label: 'Negative tweets' },
      { data: this.pos_count, label: 'Positive tweets' },
    ]
    this.lineChartLabels = this.dates;
    this.lineChartOptions = {
      responsive: true,
      scales: {
        // We use this empty structure as a placeholder for dynamic theming
        xAxes: [{}],
        yAxes: [
          {
            id: 'y-axis-0',
            position: 'left',
          },
          {
            id: 'y-axis-1',
            position: 'right',
            gridLines: {
              color: 'rgba(255,0,0,0.3)',
            },
            ticks: {
              fontColor: 'red',
            }
          }
        ]
      },
      annonation: {
        annotations: [
          {
            type: 'line',
            mode: 'vertical',
            scaleID: 'x-axis-0',
            value: 'March',
            borderColor: 'orange',
            borderWidth: 2,
            label: {
              enabled: true,
              fontColor: 'orange',
              content: 'LineAnno'
            }
          },
        ],
      }
    };
    this.lineChartLegend = true;
    this.lineChartType = 'line';
    this.graphReady = true;
  }

  ngOnInit(): void {
  }

  ngOnChanges(changes: SimpleChanges): void {
    console.log(this.graphDatas)
    this.graphReady = false;
    this.initGraph();
  }

}
