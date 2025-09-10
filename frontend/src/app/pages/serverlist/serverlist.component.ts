import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ServerCreateComponent } from './components/servercreate/servercreate.component';

@Component({
  selector: 'app-serverlist',
  standalone: true,
  imports: [CommonModule, FormsModule, ServerCreateComponent],
  templateUrl: './serverlist.component.html'
})
export class ServerlistComponent {
  imageTool = "";
  imageResource = "";

  servers = [
    { name: 'Server 1', description: 'First server', image: '/resource.png' },
    { name: 'Server 2', description: 'Second server', image: '/tool.png' }
  ];

  showCreateModal = false;

  pauseServer(index: number) { alert(`Paused: ${this.servers[index].name}`); }
  deleteServer(index: number) { this.servers.splice(index, 1); }
  editServer(index: number) { alert(`Edit: ${this.servers[index].name}`); }

  addServer(server: { name: string; description: string; serverType: string; image: string}) {
    this.servers.push({ ...server });
  }

  searchText = '';

  get filteredServers() {
    if (!this.searchText) return this.servers;
    const lower = this.searchText.toLowerCase();
    return this.servers.filter(server =>
      server.name.toLowerCase().includes(lower) ||
      server.description.toLowerCase().includes(lower)
    );
  }
}
