import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { retry, catchError, tap } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class DoorAjarService {

  // Define API
  apiURL = "https://us-central1-zokya-media.cloudfunctions.net/dooraccess?key=";

  constructor(private http: HttpClient) { }

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  }

  // HttpClient API get() method => Fetch employee
  openSesame(key): Observable<any> {
    return this.http.get<any>(this.apiURL + key)
      .pipe(
        tap( // Log the result or error
          data => {
            console.log("SUCCESS")
            return data
          },
          error => { console.log("test: " + JSON.stringify(error)) }
        )
      )
  }

  // Error handling 
  handleError(error) {
    let errorMessage = '';
    if (error.error instanceof ErrorEvent) {
      // Get client-side error
      errorMessage = error.error.message;
    } else {
      // Get server-side error
      errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
    }
    return throwError(errorMessage);
  }

}
