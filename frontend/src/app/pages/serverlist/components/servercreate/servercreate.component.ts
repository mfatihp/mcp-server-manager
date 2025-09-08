import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-server-create',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './servercreate.component.html'
})

export class ServerCreateComponent {
  @Output() serverCreated = new EventEmitter<{ name: string; description: string }>();
  @Output() close = new EventEmitter<void>();

  newServerName = '';
  newServerDesc = '';
  schemaJson = '{\n  "description": "value"\n}';
  codeFunctionName = '';
  codeArgs = '';
  codeBody = '';
  serverType = '';

  createServer() {
    if (!this.newServerName) return;
    this.serverCreated.emit({
      name: this.newServerName,
      description: this.newServerDesc
    });
    this.newServerName = '';
    this.newServerDesc = '';
  }

  cancel() {
    this.close.emit();
  }
}
