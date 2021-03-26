import { HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { StrictHttpResponse } from 'src/app/api/strict-http-response';

export const DEFAULT_DOWNLOAD_FILE_NAME = 'export';

@Injectable({
  providedIn: 'root'
})
export class BlobDownloadService {

  constructor() { }

  /**
   * Start file download from an HTTP response.
   * 
   * @param response - HTTP reponse with a file attachment
   */
  handleResponse(response: StrictHttpResponse<Blob>) {
    this.downloadBlob(response.body, this.fileName(response.headers));
  }

  /**
   * Parses the Content-Disposition header and returns the file name.
   * Return the default file name in case there is no file name defined.
   * 
   * @param headers - HTTP headers
   * @returns file name
   */
  private fileName(headers: HttpHeaders): string {
    const headerName = 'Content-Disposition';
    if (!headers.has(headerName)) {
      return DEFAULT_DOWNLOAD_FILE_NAME;
    }
    const contentDisposition = headers.get(headerName);
    const regex = /filename=([^ ;]+)/;
    try {
      return regex.exec(contentDisposition)[1];
    } catch (e) {
      return DEFAULT_DOWNLOAD_FILE_NAME;
    }
  }

  /**
   * Starts a download of the blob with the given file name.
   * 
   * @param blob - The blob to be download
   * @param fileName - The file name
   */
  private downloadBlob(blob: Blob, fileName: string) {
    const anchor = document.createElement('a');
    anchor.href = window.URL.createObjectURL(blob);
    anchor.setAttribute('download', fileName);
    document.body.appendChild(anchor);
    anchor.click();
  }
}
