import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse ,HttpHeaders} from '@angular/common/http';
import { IQuestion } from './question';
import { throwError as observableThrowError, Observable } from 'rxjs';
import { catchError } from 'rxjs/operators'

@Injectable({
  providedIn: 'root'
})

export class QuestionService {

  private _url: string = "http://localhost:5000/questions";
  private _url_next: string = "http://localhost:5000/next";

  
  constructor(private _http: HttpClient) { }

  getQuestions(sub):Observable<IQuestion[]>{
    // console.log(this._http.get<IQuestion[]>(this._url+"/"+sub))
    return this._http.get<IQuestion[]>(this._url+"/"+sub).pipe(
                      catchError(this.errorHandler)); 
  }

  errorHandler(error: HttpErrorResponse){
    return observableThrowError(error.message || "Server Error"); 
  }

  getNextQues(ques,selected){
    return this._http.post(this._url_next,{
      'question' : ques,
      'answer' : selected
    },{observe : 'response'})
  }
}
