import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { ISubject } from './subject';
import { throwError as observableThrowError, Observable } from 'rxjs';
import { catchError } from 'rxjs/operators'

@Injectable({
  providedIn: 'root'
})
export class SubjectService {

  private _url: string = "/assets/subjects.json";

  constructor(private _http: HttpClient) { }

  getSubjects():Observable<ISubject[]>{
    return this._http.get<ISubject[]>(this._url).pipe(
                      catchError(this.errorHandler)); 
  }

  errorHandler(error: HttpErrorResponse){
    return observableThrowError(error.message || "Server Error"); 
  }
}
