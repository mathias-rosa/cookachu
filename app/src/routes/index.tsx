import { createFileRoute } from '@tanstack/react-router';
import { Card, Skeleton, Typography } from '@heroui/react';
import { RecipeCard } from '@/components/RecipeCard';
import { useRecipes } from '@/hooks/use-recipes';
import { useEffect, useRef } from 'react';
import cookachuLogo from '@/assets/cookachu-logo.png';

export const Route = createFileRoute('/')({
  component: RecipesPage,
});

function RecipesPage() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
    error,
  } = useRecipes({ pageSize: 10 });

  const loadMoreRef = useRef<HTMLDivElement | null>(null);

  const recipes = data?.pages.flatMap((page) => page.items) ?? [];

  useEffect(() => {
    if (!hasNextPage) {
      return;
    }

    const node = loadMoreRef.current;
    if (!node) {
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0]?.isIntersecting && !isFetchingNextPage) {
          fetchNextPage();
        }
      },
      { rootMargin: '200px' },
    );

    observer.observe(node);
    return () => observer.disconnect();
  }, [fetchNextPage, hasNextPage, isFetchingNextPage]);

  if (isLoading) {
    return (
      <div className="mx-auto max-w-6xl px-4 py-6 md:px-6 md:py-12">
        <div className="mb-6 md:mb-8">
          <Skeleton className="h-9 w-48 rounded-lg" />
        </div>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 md:gap-6 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, index) => (
            <Card key={`recipe-skeleton-${index}`} className="p-4">
              <div className="space-y-3">
                <Skeleton className="h-5 w-3/4 rounded-lg" />
                <Skeleton className="h-4 w-full rounded-lg" />
                <Skeleton className="h-4 w-2/3 rounded-lg" />
                <div className="flex flex-wrap gap-2">
                  <Skeleton className="h-6 w-16 rounded-full" />
                  <Skeleton className="h-6 w-20 rounded-full" />
                  <Skeleton className="h-6 w-16 rounded-full" />
                </div>
                <Skeleton className="h-4 w-1/2 rounded-lg" />
              </div>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Card className="max-w-md p-6">
          <p className="text-sm">Erreur: {error.message}</p>
        </Card>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-6xl px-4 py-6 md:px-6 md:py-12">
      <div className="flex w-full items-center justify-center gap-4 md:flex-row-reverse md:justify-between md:gap-6">
        <img
          src={cookachuLogo}
          alt="Cookachu Logo"
          className="mb-4 h-20 w-20 md:mx-0"
        />
        <Typography.Heading
          level={1}
          className="font-display text-3xl font-bold"
        >
          Mes Recettes
        </Typography.Heading>
      </div>

      {recipes.length === 0 ? (
        <Card className="p-6">
          <p className="text-center text-sm">Aucune recette trouvée.</p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {recipes.map((record) => (
            <RecipeCard
              record={record}
              key={record.id ?? record.recipe.title}
            />
          ))}
        </div>
      )}

      {hasNextPage ? <div ref={loadMoreRef} /> : null}
    </div>
  );
}
