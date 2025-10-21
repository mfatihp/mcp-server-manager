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
  private mcpCheckListUrl = 'http://localhost:8000/manager/check_list';

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

  getServers() {
    this.http.get(this.mcpCheckListUrl, {});
    return this.servers;
  }

  runMCPServer(server: ServerItem) { 
    // TODO: Pause & Play, pause tuşu bir kere basıldığında pause butonu değişecek ve play butonu olacak. Ona göre de işlev eklenecek

    this.http.post(this.mcpControlUrl, {
                                        serverId: "",
                                        controlCommand: "pause"
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
                                        serverId: "",
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
                                        serverId: "",
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
    // Show in UI immediately
    const current = this.serversSubject.value;
    this.serversSubject.next([...current, server]);

    this.mcp_schema = {"server_name": server.name, 
                        "description": server.description,
                        "servertype": server.serverType,
                        "pkgs": server.pkgs,
                        "func_args": server.func_args, 
                        "func_body": server.func_body, 
                      }

    this.http.post(this.mcpCreateUrl, this.mcp_schema).subscribe({
                                                            next: (response) => {
                                                              console.log("Success:", response);
                                                              server.pending = false;
                                                            },
                                                            error: (error) => {
                                                              console.log("Error:", error);
                                                              server.pending = false;
                                                            }
                                                          });
  }
}
