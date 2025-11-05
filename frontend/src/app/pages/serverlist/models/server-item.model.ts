export interface ServerItem {
  contID: string;
  name: string;
  description: string;
  serverType: string;
  image: string;
  pkgs: string[];
  func_args: string;
  func_body: string;
  pending: boolean;
  IsRunning: boolean;
}