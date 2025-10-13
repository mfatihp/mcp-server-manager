import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class LlmchatService {
  private mcpCheckListUrl = 'http://localhost:8000/manager/get_list';
  private mcpCheckLogsUrl = 'http://localhost:8090/log_list';
  private llmChatUrl = 'http://localhost:8000/chat';

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

  getAnswer(messages : { sender: 'user' | 'bot'; text: string }[]) {
    const messageText = this.userInput.trim();
    if (!messageText) return; // Ignore empty input

    // Append user's message to chat history
    messages.push({ sender: 'user', text: messageText });
    this.userInput = '';

    const text = messageText;

    // Send the message to the FastAPI backend and handle the response
    this.http.post<{ reply: string }>(this.llmChatUrl, { text })
      .subscribe({
        next: (response) => {
          // Add the bot's reply to the chat history
          messages.push({ sender: 'bot', text: response.reply });
        },
        error: (err) => {
          // Add an error message to the chat if the backend request fails
          messages.push({ sender: 'bot', text: 'Error: could not get a reply.' });
          console.error(err);
        }
      });
  }
}
