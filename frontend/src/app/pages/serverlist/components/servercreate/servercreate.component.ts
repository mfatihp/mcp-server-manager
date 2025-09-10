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
  @Output() serverCreated = new EventEmitter<{ name: string; description: string; serverType: string; image: string;}>();
  @Output() close = new EventEmitter<void>();

  newServerName = '';
  newServerDesc = '';
  schemaJson = '{\n  "description": "value"\n}';
  codeFunctionName = '';
  codeArgs = '';
  codeBody = '';
  servertype = '';
  images: Record<string, string> = {
    tool: '/tool.png',
    resource: '/resource.png'
  };

  createServer() {
    if (!this.newServerName) return;
    this.serverCreated.emit({
      name: this.newServerName,
      description: this.newServerDesc,
      serverType: this.servertype,
      image: this.images[this.servertype]
    });
    this.newServerName = '';
    this.newServerDesc = '';
  }

  cancel() {
    this.close.emit();
  }
}
