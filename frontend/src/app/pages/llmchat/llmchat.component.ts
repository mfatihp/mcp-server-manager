import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { LlmchatService } from './llmchat.service';
import { ViewChild, ElementRef } from '@angular/core';


type LogEntry = {
  serverName: string;
  actionTime: string; 
}


@Component({
  selector: 'app-llmchat',
  imports: [CommonModule, FormsModule],
  standalone: true,
  templateUrl: './llmchat.component.html'
})
export class LlmchatComponent {
  @ViewChild('chatMessages') private chatMessagesRef!: ElementRef;
  constructor(private service: LlmchatService) {}

  userInput: string = '';
  messages: { sender: 'user' | 'bot'; text: string }[] = [];
  servers: { name: string }[] = [];

  mcpLogs: string[] = [];
  rawEntries: { serverName: string; actionTime: string }[] = [];

  activeTab: 'servers' | 'logs' = 'servers';

  formatList(items: LogEntry[]) {
    items.forEach((item) => {
      this.mcpLogs.push(`${item.serverName} is called at ${item.actionTime}`);
    })
  }

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  scrollToBottom() {
    try {
      this.chatMessagesRef.nativeElement.scrollTop = this.chatMessagesRef.nativeElement.scrollHeight;
    } catch (err) {
      console.error('Scroll failed:', err);
    }
  }

  sendMessage() {
    this.service.getAnswer(this.messages);
    this.scrollToBottom();
  }

  getServerList() {}

  getServerLogs() {
    this.service.getLogs(this.rawEntries);
    this.formatList(this.rawEntries);
  }
}
