import { Component, OnInit } from '@angular/core';
import { ResultService } from '../result.service';
import { ActivatedRoute } from '@angular/router';
import { from } from 'rxjs';
import {Router} from "@angular/router";


@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent implements OnInit {

  public graphs = [];
  response : any;
  show : boolean = false;
  count : number;
  constructor(private _resultService :ResultService,private _route: ActivatedRoute,private router: Router) { 
    setTimeout(() => {
      this.show = true;
    }, 10000);
  }
  

  ngOnInit() {
    let uname = this._route.snapshot.paramMap.get('name');
    console.log('---in results got uname as',uname);

    this._resultService.getRes(uname).subscribe(data => {
      console.log(data);
      this.response = JSON.parse(JSON.stringify(data));
      // this.graphs.push(this.response.body[0]);
      this.graphs = this.response.body;
      console.log('---resp---',this.response.body);
      // this.graphs.push(this.response.body[1]);
    })
  }

  // timeout(){
  //   this.count = 0;
  //   while(this.count<=1000000000)
  //   {
  //     this.count = this.count+1;
  //   }
  //  this.show = true;
  // }

}
