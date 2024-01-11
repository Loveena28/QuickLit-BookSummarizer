import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment as env } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class BackendApiService {
  constructor(private http: HttpClient) {}
  summarizeImage(file: File) {
    console.log(file)
    const formData = new FormData();
    formData.append('image', file);
    return this.http.post<Result>(env.baseUrl + 'ocr', formData);
  }
}
export interface Result {
  title: string;
  author: string;
  summary: string;
}
