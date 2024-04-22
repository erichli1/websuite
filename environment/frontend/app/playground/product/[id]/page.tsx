"use client";

import { Typography } from "@mui/material";
import { getSearchProduct, navigateTo } from "../../playgroundUtils";
import LoggedButton from "@/ui/components/click/button/LoggedButton";
import { useRouter } from "next/navigation";

export default function Page({ params }: { params: { id: string } }) {
  const product = getSearchProduct(params.id);

  const router = useRouter();

  if (!product) return <Typography>This product does not exist.</Typography>;

  return (
    <>
      <Typography variant="h5">{product.name}</Typography>
      <Typography variant="body1">
        {product.rating} stars ({product.numRatings} reviews)
      </Typography>

      <Typography variant="h6">${product.price.toFixed(2)}</Typography>

      <div>
        <LoggedButton
          logLabel="Buy now"
          variant="contained"
          onClick={() => navigateTo({ router, url: "/playground/checkout" })}
        />
      </div>
    </>
  );
}
