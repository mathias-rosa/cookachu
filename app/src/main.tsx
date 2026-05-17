import '@fontsource-variable/arima/wght.css';
import '@fontsource-variable/inter/wght.css';
import './global.css';

import { QueryClientProvider } from '@tanstack/react-query';
import { RouterProvider, createRouter } from '@tanstack/react-router';
import { StrictMode } from 'react';
import ReactDOM from 'react-dom/client';

// Import the generated route tree
import TypesafeI18n from './i18n/i18n-react';
import { baseLocale } from './i18n/i18n-util';
import { loadLocale } from './i18n/i18n-util.sync';
import { queryClient } from './lib/query-client';
import { routeTree } from './routeTree.gen';

loadLocale(baseLocale);

// Create a new router instance
const router = createRouter({
  routeTree,
  context: {
    queryClient,
  },
});

// Register the router instance for type safety
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router;
  }
}

// Render the app
const rootElement = document.getElementById('root')!;
if (!rootElement.innerHTML) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <StrictMode>
      <TypesafeI18n locale={baseLocale}>
        <QueryClientProvider client={queryClient}>
          <RouterProvider router={router} />
        </QueryClientProvider>
      </TypesafeI18n>
    </StrictMode>,
  );
}
