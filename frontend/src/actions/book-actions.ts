import { bookService } from '@/services/book-service';

export const bookActions = {
  listAvailableBooks() {
    return bookService.listAvailableBooks();
  },
  borrowBook(bookId: number) {
    return bookService.borrowBook(bookId);
  },
  getBorrowHistory() {
    return bookService.getBorrowHistory();
  },
  returnBook(borrowId: number) {
    return bookService.returnBook(borrowId);
  },
};
