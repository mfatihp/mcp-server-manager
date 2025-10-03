import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ServerCreateComponent } from './components/servercreate/servercreate.component';
import { ServerlistService } from './serverlist.service';
import { ServerItem } from './models/server-item.model';

@Component({
  selector: 'app-serverlist',
  standalone: true,
  imports: [CommonModule, FormsModule, ServerCreateComponent],
  templateUrl: './serverlist.component.html'
})

export class ServerlistComponent implements OnInit {
  constructor(private service: ServerlistService) {}

  //servers!: { name: string, description: string, image: string; pending: boolean; IsRunning: boolean}[];
  servers: ServerItem[] = [];

  ngOnInit(): void {
    this.servers = this.service.getServers();
  }


  showCreateModal = false;

  pauseServer(server: { name: string; 
                      description: string; 
                      serverType: string; 
                      image: string; 
                      pkgs: string[]; 
                      func_args: string; 
                      func_body: string;
                      pending: boolean;
                      IsRunning: boolean;
                    }) {
    if (server.IsRunning == false) {
      this.service.pauseMCPServer(server);
    } else {
      this.service.runMCPServer(server);
    }
  }
  
  deleteServer(index: number) { 
    this.servers.splice(index, 1); 
    this.service.deleteMCPServer(index); // TODO: Container işlemlerinin tamamlanması gerekiyor. arg olarak contID olacak.
  }
  
  editServer(index: number) { 
    alert(`Edit: ${this.servers[index].name}`); 
  }

  addServer(server: { name: string; 
                      description: string; 
                      serverType: string; 
                      image: string; 
                      pkgs: string[]; 
                      func_args: string; 
                      func_body: string;
                      pending: boolean;
                      IsRunning: boolean;
                    }) {
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
