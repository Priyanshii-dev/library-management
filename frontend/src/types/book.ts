export interface BookItem {
  id: number;
  title: string;
  author: string;
  price: number;
  availability: string;
  available_quantity: number;
}

export type BookListResponse = BookItem[] | {
  items?: BookItem[];
  data?: BookItem[];
};
