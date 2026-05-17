import { useI18nContext } from './i18n-react';

import type { components } from '@/api/types';

type Appliance = components['schemas']['Appliance'];
type CuisineType = components['schemas']['CuisineType'];
type Difficulty = components['schemas']['Difficulty'];
type DishType = components['schemas']['DishType'];

export const useEnumLabels = () => {
  const { LL } = useI18nContext();

  return {
    appliance: (value: Appliance) => LL.enums.appliance[value](),
    cuisineType: (value: CuisineType) => LL.enums.cuisineType[value](),
    difficulty: (value: Difficulty) => LL.enums.difficulty[value](),
    dishType: (value: DishType) => LL.enums.dishType[value](),
  };
};
