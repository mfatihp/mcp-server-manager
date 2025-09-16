import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ServerCreateComponent } from './components/servercreate/servercreate.component';
import { ServerlistService } from './serverlist.service';

@Component({
  selector: 'app-serverlist',
  standalone: true,
  imports: [CommonModule, FormsModule, ServerCreateComponent],
  templateUrl: './serverlist.component.html'
})

export class ServerlistComponent implements OnInit {
  constructor(private service: ServerlistService) {}

  servers!: { name: string, description: string, image: string}[];

  ngOnInit(): void {
    this.servers = this.service.getServers();
  }


  showCreateModal = false;

  pauseServer(index: number) { 
    alert(`Paused: ${this.servers[index].name}`); 
    this.service.pauseMCPServer(index, this.servers[index].name); // TODO: Create message body, replace name property
  }
  
  deleteServer(index: number) { 
    this.servers.splice(index, 1); 
  }
  
  editServer(index: number) { 
    alert(`Edit: ${this.servers[index].name}`); 
  }

  addServer(server: { name: string; description: string; serverType: string; image: string}) {
    this.servers.push({ ...server });
    this.service.addMCPServer(server);
  }

  // Search and filter
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
