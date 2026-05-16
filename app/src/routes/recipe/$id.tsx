import { createFileRoute } from '@tanstack/react-router';
import { Card, Skeleton } from '@heroui/react';
import { RecipeDetail } from '@/components/RecipeDetail';
import { useRecipe } from '@/hooks/use-recipe';

export const Route = createFileRoute('/recipe/$id')({
  component: RecipePage,
});

function RecipePage() {
  const { id } = Route.useParams();
  const { data, isLoading, error } = useRecipe(id);

  if (isLoading) {
    return (
      <div className="mx-auto max-w-5xl space-y-6 px-4 py-6 md:px-6 md:py-12">
        <Card className="space-y-4 p-6">
          <Skeleton className="h-8 w-2/3 rounded-lg" />
          <Skeleton className="h-4 w-full rounded-lg" />
          <Skeleton className="h-4 w-5/6 rounded-lg" />
          <div className="flex flex-wrap gap-2">
            {Array.from({ length: 4 }).map((_, index) => (
              <Skeleton
                key={`recipe-meta-${index}`}
                className="h-6 w-24 rounded-full"
              />
            ))}
          </div>
        </Card>
        <div className="grid gap-6 md:grid-cols-2">
          {Array.from({ length: 2 }).map((_, index) => (
            <Card key={`recipe-section-${index}`} className="space-y-3 p-6">
              <Skeleton className="h-6 w-40 rounded-lg" />
              <Skeleton className="h-4 w-full rounded-lg" />
              <Skeleton className="h-4 w-5/6 rounded-lg" />
              <Skeleton className="h-4 w-4/6 rounded-lg" />
            </Card>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mx-auto max-w-5xl px-4 py-6 md:px-6 md:py-12">
        <Card className="p-6">
          <p className="text-sm">Erreur: {error.message}</p>
        </Card>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="mx-auto max-w-5xl px-4 py-6 md:px-6 md:py-12">
        <Card className="p-6">
          <p className="text-sm">Recette non trouvee.</p>
        </Card>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-6 md:px-6 md:py-12">
      <RecipeDetail record={data} />
    </div>
  );
}
