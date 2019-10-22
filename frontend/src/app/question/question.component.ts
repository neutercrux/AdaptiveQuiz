import { Component, OnInit } from '@angular/core';
import { QuestionService } from '../question.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-question',
  templateUrl: './question.component.html',
  styleUrls: ['./question.component.css']
})
export class QuestionComponent implements OnInit {

  public questions = []
  public errorMsg;
  constructor(private _questionService: QuestionService, private _route: ActivatedRoute) { }

  ngOnInit() {

    let name = this._route.snapshot.paramMap.get('name');

    this._questionService.getQuestions()
      .subscribe(data => this.questions = data,
                 error => this.errorMsg = error);
  }

}
