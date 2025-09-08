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
  servers = [
    { name: 'Server 1', description: 'First server', image: 'https://via.placeholder.com/150' },
    { name: 'Server 2', description: 'Second server', image: 'https://via.placeholder.com/150' }
  ];

  showCreateModal = false;

  pauseServer(index: number) { alert(`Paused: ${this.servers[index].name}`); }
  deleteServer(index: number) { this.servers.splice(index, 1); }
  editServer(index: number) { alert(`Edit: ${this.servers[index].name}`); }

  addServer(server: { name: string; description: string }) {
    this.servers.push({ ...server, image: 'https://via.placeholder.com/150' });
  }
}
