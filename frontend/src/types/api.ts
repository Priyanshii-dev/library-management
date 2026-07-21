export interface ApiResponse<T = unknown> {
  error: boolean;
  message: string;
  statusCode: number;
  data: T;
}
