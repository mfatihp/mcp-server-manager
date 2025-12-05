import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ServerItem } from './models/server-item.model';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ServerlistService {
  private serversSubject = new BehaviorSubject<ServerItem[]>([]);
  servers$ = this.serversSubject.asObservable();

  private mcpCreateUrl = 'http://localhost:8000/manager/create_mcp_server';
  private mcpControlUrl = 'http://localhost:8000/manager/control_mcp_server';
  private mcpCheckListUrl = 'http://localhost:8090/log_list';
  private mcpCheckLogUrl = 'http://localhost:8090/log_list';

  mcp_schema!: {
    "server_name": string, 
    "description": string, 
    "func_args": string, 
    "func_body": string, 
    "servertype": string; 
    "pkgs": string[] 
  };

  constructor(private http: HttpClient) { }

  servers: ServerItem[] = [];

  async getServers() {
    console.log("hey");
    // const response = await fetch(this.mcpCheckListUrl, {method: "GET"});
    // console.log(response);
    // return this.servers;
  }

  runMCPServer(server: ServerItem) { 
    // TODO: Pause & Play, pause tuşu bir kere basıldığında pause butonu değişecek ve play butonu olacak. Ona göre de işlev eklenecek

    this.http.post(this.mcpControlUrl, {
                                        serverId: server.contID,
                                        controlCommand: "run",
                                        controlParams: {}
                                      }).subscribe({
                                                next: (response) => {
                                                  console.log("Success:", response);
                                                  server.IsRunning = true;
                                                },
                                                error: (error) => {
                                                  console.log("Error:", error);
                                                }
                                              });
  }

  pauseMCPServer(server: ServerItem) { 
    // TODO: Pause & Play, pause tuşu bir kere basıldığında pause butonu değişecek ve play butonu olacak. Ona göre de işlev eklenecek

    this.http.post(this.mcpControlUrl, {
                                        serverId: server.contID,
                                        controlCommand: "pause"
                                      }).subscribe({
                                                next: (response) => {
                                                  console.log("Success:", response);
                                                  server.IsRunning = false;
                                                },
                                                error: (error) => {
                                                  console.log("Error:", error);
                                                }
                                              });
  }
  
  deleteMCPServer(server: ServerItem) { 

    this.http.post(this.mcpControlUrl, {
                                        serverId: server.contID,
                                        controlCommand: "delete"
                                      }).subscribe({
                                                  next: (response) => {
                                                    console.log("Success:", response);
                                                  },
                                                  error: (error) => {
                                                    console.log("Error:", error);
                                                  }
                                                });
  }

  addMCPServer(server: ServerItem) {
    server.pending = true;
    const current = this.serversSubject.value;

    // ➜ Immediately add to list so UI shows it
    this.serversSubject.next([...current, server]);

    this.mcp_schema = {
      "server_name": server.name,
      "description": server.description,
      "servertype":  server.serverType,
      "pkgs":        server.pkgs,
      "func_args":   server.func_args,
      "func_body":   server.func_body,
    }

    this.http.post<any>(this.mcpCreateUrl, this.mcp_schema).subscribe({
      next: (response) => {
        console.log("Success:", response);
        server.contID = response.contID,
        server.pending = false;

        // Trigger UI update
        this.serversSubject.next([...this.serversSubject.value]);
      },
      error: (error) => {
        console.log("Error:", error);
        server.pending = false;
        // 3. Remove the created UI item if request fails
        const updated = this.serversSubject
          .value
          .filter(s => s !== server);

        this.serversSubject.next(updated);
      }
    });
  }
}
