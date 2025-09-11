import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';


interface Message {
  text: string;
  sender: 'me' | 'bot';
}


@Component({
  selector: 'app-llmchat',
  imports: [CommonModule, FormsModule],
  standalone: true,
  templateUrl: './llmchat.component.html'
})
export class LlmchatComponent {
  messages: Message[] = [
    { text: 'Hi! 👋', sender: 'bot' },
    { text: 'Hello! How are you?', sender: 'me' }
  ];
  newMessage: string = '';

  activeTab: 'servers' | 'logs' = 'servers';

  servers = [
    { name: 'Server 1' },
    { name: 'Server 2' },
    { name: 'Server 3' }
  ];

  logs = [
    'Server 1 started at 10:05',
    'Server 2 paused at 10:15',
    'Server 3 deleted at 10:30'
  ];

  sendMessage() {
    if (!this.newMessage.trim()) return;

    // Add user message
    this.messages.push({ text: this.newMessage, sender: 'me' });

    const userMsg = this.newMessage;
    this.newMessage = '';

    // Mock bot reply
    setTimeout(() => {
      this.messages.push({ text: `You said: "${userMsg}"`, sender: 'bot' });
    }, 800);
  }
}
