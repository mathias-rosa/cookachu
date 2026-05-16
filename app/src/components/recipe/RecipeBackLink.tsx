import { Link } from '@tanstack/react-router';
import { ArrowLeft } from 'lucide-react';

export const RecipeBackLink = () => (
  <Link
    to="/"
    className="link text-muted hover:text-foreground inline-flex items-center gap-2 text-sm"
  >
    <ArrowLeft size={16} />
    Retour aux recettes
  </Link>
);
