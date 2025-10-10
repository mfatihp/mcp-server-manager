import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ServerItem } from '../serverlist/models/server-item.model';

@Injectable({
  providedIn: 'root'
})

export class LlmchatService {
  private mcpCheckListUrl = 'http://localhost:8000/manager/get_list';
  private mcpCheckLogsUrl = 'http://localhost:8000/manager/get_logs';
  private llmChatUrl = 'http://localhost:8000/chat';

  constructor(private http: HttpClient) { }

  servers: ServerItem[] = [];

  getServers() {
    this.http.get(this.mcpCheckListUrl, {});
    return this.servers;
  }

  getLogs() {
    this.http.get(this.mcpCheckLogsUrl, {});
    return this.servers;
  }

  getAnswer() {
    this.http.get(this.llmChatUrl, {});
    return this.servers;
  }
}
