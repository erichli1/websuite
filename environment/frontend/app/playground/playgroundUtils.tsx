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

  return PLAYGROUND_PRODUCTS.filter(
    (product) =>
      matchSubstrings(product.name.toLowerCase(), keywords.toLowerCase()) ||
      matchSubstrings(
        product.description.toLowerCase(),
        keywords.toLowerCase()
      ) ||
      product.keywords.some((productKeyword) =>
        productKeyword.toLowerCase().includes(keywords.toLowerCase())
      )
  );
}

function matchSubstrings(word1: string, word2: string): boolean {
  let word1Words = word1.toLowerCase().split(" ");
  let word2Array = word2.toLowerCase().split(" ");

  return word2Array.some((keyword) =>
    word1Words.some((word) => word.includes(keyword))
  );
}

export function getSearchProduct(id: string) {
  return PLAYGROUND_PRODUCTS.find((product) => product.id === id);
}

export type SelectedCustomization = {
  [key: string]: string;
};
