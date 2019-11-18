import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class ResultService {
  private _url:string = "http://localhost:5000/results/"
  constructor(private http : HttpClient) { }

  getRes(uname){
    return this.http.get(this._url+uname,{observe : 'response'})
  }
}
