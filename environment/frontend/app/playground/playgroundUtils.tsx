import { navigate } from "@/ui/log";
import { AppRouterInstance } from "next/dist/shared/lib/app-router-context.shared-runtime";
import { PLAYGROUND_PRODUCTS } from "../data";

export function navigateTo({
  router,
  url,
}: {
  router: AppRouterInstance;
  url: string;
}) {
  navigate({ url }).then(() => {
    router.push(url);
  });
}

export function searchProducts(keywords: string | null) {
  if (!keywords) {
    return [];
  }

  return PLAYGROUND_PRODUCTS.filter((product) =>
    product.name.toLowerCase().includes(keywords.toLowerCase())
  );
}

export function getSearchProduct(id: string) {
  return PLAYGROUND_PRODUCTS.find((product) => product.id === id);
}
