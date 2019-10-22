import { Component, OnInit } from '@angular/core';
import { SubjectService } from '../subject.service';
import { ISubject } from '../subject';
import { Router } from '@angular/router';

@Component({
  selector: 'app-subject',
  templateUrl: './subject.component.html',
  styleUrls: ['./subject.component.css']
})
export class SubjectComponent implements OnInit {

  public subjects = []
  public errorMsg;
  constructor(private _subjectService: SubjectService, private _router: Router) { }

  ngOnInit() {
    this._subjectService.getSubjects()
      .subscribe(data => this.subjects = data,
                 error => this.errorMsg = error);
  }

  onselect(subject){
    this._router.navigate(['/subject', subject.name])
  }
}
