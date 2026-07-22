import { apiClient } from '@/services/api-client';
import type { UserProfile } from '@/types/auth';

export const adminService = {
  async getPendingApprovals(skip = 0, limit = 20) {
    return apiClient.get<UserProfile[]>(`/admin/pending-approvals?skip=${skip}&limit=${limit}`);
  },

  async approveUser(userId: number) {
    return apiClient.post<{ message: string; user: UserProfile }>(`/admin/approve/${userId}`);
  },
  
  async rejectUser(userId: number) {
    return apiClient.post<{ message: string; user: UserProfile }>(`/admin/reject/${userId}`);
  },

  async getDashboardStats() {
    return apiClient.get<any>(`/admin/dashboard/stats`);
  },

  async createCategory(data: { name: string; description?: string }) {
    return apiClient.post<any>(`/admin/categories`, data);
  },

  async listCategories() {
    return apiClient.get<any[]>(`/admin/categories`);
  },

  async createBook(data: { title: string; author: string; price: number; category_id: number; total_quantity: number }) {
    return apiClient.post<any>(`/admin/book/create`, data);
  },

  async listBooks(params?: { page?: number; limit?: number; search?: string }) {
    const qs = new URLSearchParams();
    if (params?.page) qs.set('page', String(params.page));
    if (params?.limit) qs.set('limit', String(params.limit));
    if (params?.search) qs.set('search', params.search);
    return apiClient.get<any[]>(`/admin/book/list?${qs.toString()}`);
  },

  async updateBook(bookId: number, data: Partial<{ title: string; author: string; price: number; category_id: number; total_quantity: number; available_quantity: number }>) {
    return apiClient.patch<any>(`/admin/book/update/${bookId}`, data);
  },

  async deleteBook(bookId: number) {
    return apiClient.delete<any>(`/admin/book/delete/${bookId}`);
  },
};
