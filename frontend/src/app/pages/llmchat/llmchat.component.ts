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
  @ViewChild('chatMessages', { static: false }) private chatMessagesRef!: ElementRef;

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
    // Safe check
    if (!this.chatMessagesRef?.nativeElement) return;

    try {
      // Scroll with a tiny delay for async rendering
      setTimeout(() => {
        this.chatMessagesRef.nativeElement.scrollTop = this.chatMessagesRef.nativeElement.scrollHeight;
      }, 0);
    } catch (err) {
      console.error('Scroll failed:', err);
    }
  }

  async sendMessage() {
    const text = this.userInput.trim();
    if (!text) return;

    // Add user message immediately
    this.messages.push({ sender: 'user', text });
    this.userInput = '';

    // Get bot reply
    const reply = await this.service.getAnswer(text);
    this.messages.push({ sender: 'bot', text: reply });

    this.scrollToBottom();
  }

  getServerList() {}

  getServerLogs() {
    this.service.getLogs(this.rawEntries);
    this.formatList(this.rawEntries);
  }
}
