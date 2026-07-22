'use client';

import { useState, useEffect } from 'react';
import { adminService } from '@/services/admin-service';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { toast } from '@/lib/toast';
import { Loader2, Plus } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';

export function AddBookModal() {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [categories, setCategories] = useState<any[]>([]);

  const [formData, setFormData] = useState({
    title: '',
    author: '',
    price: '',
    category_id: '',
    total_quantity: '',
  });

  const [categoryData, setCategoryData] = useState({
    name: '',
    description: '',
  });

  useEffect(() => {
    if (isOpen) {
      adminService.listCategories().then((res) => {
        setCategories(res.data || []);
      });
    }
  }, [isOpen]);

  const handleCreateCategory = async () => {
    if (!categoryData.name) {
      toast({ type: 'error', message: 'Category name is required' });
      return;
    }
    
    try {
      setIsLoading(true);
      const res = await adminService.createCategory(categoryData);
      toast({ type: 'success', message: 'Category created!' });
      setCategories([...categories, res.data]);
      setCategoryData({ name: '', description: '' });
      if (res.data?.id) {
        setFormData({ ...formData, category_id: res.data.id.toString() });
      }
    } catch (error: any) {
      toast({ type: 'error', message: error.message || 'Failed to create category' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.title || !formData.author || !formData.price || !formData.category_id || !formData.total_quantity) {
      toast({ type: 'error', message: 'All fields are required' });
      return;
    }

    try {
      setIsLoading(true);
      await adminService.createBook({
        title: formData.title,
        author: formData.author,
        price: parseFloat(formData.price),
        category_id: parseInt(formData.category_id),
        total_quantity: parseInt(formData.total_quantity),
      });
      toast({ type: 'success', message: 'Book created successfully!' });
      setIsOpen(false);
      setFormData({ title: '', author: '', price: '', category_id: '', total_quantity: '' });
      // Optionally trigger a re-fetch of stats or books here
    } catch (error: any) {
      toast({ type: 'error', message: error.message || 'Failed to create book' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button className="gap-2">
          <Plus size={16} /> Add Book
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Add New Book</DialogTitle>
          <DialogDescription>
            Add a new book to the library catalog.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4 py-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Title</Label>
              <Input 
                value={formData.title} 
                onChange={(e) => setFormData({...formData, title: e.target.value})} 
                placeholder="Book title" 
              />
            </div>
            <div className="space-y-2">
              <Label>Author</Label>
              <Input 
                value={formData.author} 
                onChange={(e) => setFormData({...formData, author: e.target.value})} 
                placeholder="Author name" 
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Price ($)</Label>
              <Input 
                type="number" 
                step="0.01" 
                value={formData.price} 
                onChange={(e) => setFormData({...formData, price: e.target.value})} 
                placeholder="29.99" 
              />
            </div>
            <div className="space-y-2">
              <Label>Total Quantity</Label>
              <Input 
                type="number" 
                value={formData.total_quantity} 
                onChange={(e) => setFormData({...formData, total_quantity: e.target.value})} 
                placeholder="5" 
              />
            </div>
          </div>

          <div className="space-y-2 pt-2 border-t border-white/10 mt-4">
            <Label>Category</Label>
            {categories.length > 0 ? (
              <select 
                className="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                value={formData.category_id}
                onChange={(e) => setFormData({...formData, category_id: e.target.value})}
              >
                <option value="">Select a category...</option>
                {categories.map((c) => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            ) : (
              <div className="text-sm text-amber-500 mb-2">No categories found. Create one first!</div>
            )}
          </div>

          <div className="p-3 bg-white/5 rounded-md space-y-3 mt-2 border border-white/10">
            <Label className="text-xs text-muted-foreground uppercase">Quick Add Category</Label>
            <div className="flex gap-2">
              <Input 
                placeholder="New Category Name" 
                value={categoryData.name}
                onChange={(e) => setCategoryData({...categoryData, name: e.target.value})}
              />
              <Button type="button" variant="secondary" onClick={handleCreateCategory} disabled={isLoading}>
                Add
              </Button>
            </div>
          </div>

          <DialogFooter className="pt-4">
            <Button type="button" variant="outline" onClick={() => setIsOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Save Book
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
