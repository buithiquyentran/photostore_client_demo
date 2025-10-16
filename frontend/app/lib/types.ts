export interface ApiCredentials {
  apiKey: string;
  apiSecret: string;
  baseUrl: string;
}

export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  stock: number;
  status: "active" | "draft" | "archived";
  category?: string;
  image?: string;
  createdAt: string;
  updatedAt: string;
}

export interface ApiResponse<T = any> {
  data: T;
  status: number;
  timestamp: string;
  signature: string;
}
