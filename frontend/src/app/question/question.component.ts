import { Component, OnInit } from '@angular/core';
import { QuestionService } from '../question.service';
import { ActivatedRoute } from '@angular/router';
import { IQuestion} from '../question';
import { from } from 'rxjs';
import {Router} from "@angular/router";
import { NgForm } from '@angular/forms';
import { MDBBtn, MDBIcon } from "mdbreact";


@Component({
  selector: 'app-question',
  templateUrl: './question.component.html',
  styleUrls: ['./question.component.css']
})
export class QuestionComponent implements OnInit {

  public questions = [];
  public errorMsg;
  response:any;
  available = true;
  constructor(private _questionService: QuestionService, private _route: ActivatedRoute,private router: Router) { }

  ngOnInit() {

    let name = this._route.snapshot.paramMap.get('name');

    this._questionService.getQuestions(name)
      .subscribe(data => {
                  this.questions = data;
                },
                 error => this.errorMsg = error);
    console.log(this.questions);
  }
  clicked : any
  getNext(){

    let selected = this.clicked;
    console.log(this.clicked);
    let ques = this.questions[0].question;
    this._questionService.getNextQues(ques,selected).subscribe(data =>{
      this.response = JSON.parse(JSON.stringify(data));
      // console.log(this.response.body);
      if(this.response.status==200){
        this.questions = Array(this.response.body);
        this.clicked = false;
      }
      else{
        console.log(this.response.body);
        this.available = false;
      }
    })
  }

  getResults(){
    this.router.navigate(['/results'])
  }
}


