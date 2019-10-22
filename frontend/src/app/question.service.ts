import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { IQuestion } from './question';
import { throwError as observableThrowError, Observable } from 'rxjs';
import { catchError } from 'rxjs/operators'

@Injectable({
  providedIn: 'root'
})
export class QuestionService {

  private _url: string = "/assets/questions.json";

  constructor(private _http: HttpClient) { }

  getQuestions():Observable<IQuestion[]>{
    return this._http.get<IQuestion[]>(this._url).pipe(
                      catchError(this.errorHandler)); 
  }

  errorHandler(error: HttpErrorResponse){
    return observableThrowError(error.message || "Server Error"); 
  }
}
