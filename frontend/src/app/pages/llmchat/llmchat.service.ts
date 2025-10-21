import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { lastValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class LlmchatService {
  private mcpCheckListUrl = 'http://localhost:8000/manager/get_list';
  private mcpCheckLogsUrl = 'http://localhost:8090/log_list';
  private llmChatUrl = 'http://localhost:8070/chat';

  constructor(private http: HttpClient) { }

  userInput: string = '';

  getServers(servers: { name: string }[]) {
    this.http.post(this.mcpCheckListUrl, {}).subscribe({
                                                next: (response) => {
                                                  console.log("Success:", response);
                                                },
                                                error: (error) => {
                                                  console.log("Error:", error);
                                                }
                                              });
                                              
    return servers; // TODO: Gerek var mı diye bakılacak
  }

  getLogs(logs: { serverName: string; actionTime: string }[]) {
    this.http.get(this.mcpCheckLogsUrl, {}).subscribe({
                                                next: (response) => {
                                                  console.log("Success:", response);
                                                },
                                                error: (error) => {
                                                  console.log("Error:", error);
                                                }
                                              });
    return logs;
  }

  async getAnswer(userText: string): Promise<string> {
    const text = userText.trim();
    if (!text) return '';

    try {
      const response = await lastValueFrom(
        this.http.post<{ reply: string }>(this.llmChatUrl, { text })
      );
      return response.reply;
    } catch (err) {
      console.error('Error fetching reply:', err);
      return 'Error: could not get a reply.';
    }
  }
}
