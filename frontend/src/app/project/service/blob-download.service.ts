import { HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { StrictHttpResponse } from 'src/app/api/strict-http-response';

@Injectable({
  providedIn: 'root'
})
export class BlobDownloadService {

  constructor() { }

  handleResponse(response: StrictHttpResponse<Blob>) {
    this.downloadBlob(response.body, this.fileName(response.headers));
  }

  private fileName(headers: HttpHeaders): string {
    const contentDisposition = headers.get('Content-Disposition');
    const regex = /filename=([^ ;]+)/;
    try {
      return regex.exec(contentDisposition)[1];
    } catch (e) {
      return 'export';
    }
  }

  private downloadBlob(blob: Blob, fileName: string) {
    const anchor = document.createElement('a');
    anchor.href = window.URL.createObjectURL(blob);
    anchor.setAttribute('download', fileName);
    document.body.appendChild(anchor);
    anchor.click();
  }
}
