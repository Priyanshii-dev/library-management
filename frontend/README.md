# LibraryHub Frontend

Production Next.js frontend for the Library Management System.

## Structure

- `app/` - App Router pages and global styles.
- `src/lib/` - Shared API client, proxy helpers, and validation schemas.
- `src/store/` - Client-side application state.
- `public/` - Static assets served by Next.js.

## Scripts

```bash
npm run dev
npm run build
npm run start
```

By default, browser requests to `/api/v1/*` are rewritten to `http://127.0.0.1:8000/api/v1/*`.
Set `NEXT_PUBLIC_BACKEND_URL` to point the frontend at a different backend host.
