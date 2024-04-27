"use client";

import { FormContainer } from "@/ui/containers/Forms";
import { Typography } from "@mui/material";
import {
  SelectedCustomization,
  getSearchProduct,
  navigateTo,
} from "../playgroundUtils";
import { useRouter, useSearchParams } from "next/navigation";
import React from "react";
import { stringifyJsonSortKeys } from "@/ui/log";

export default function Page() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const cartSearchParam = searchParams.get("cart");

  const [productId, setProductId] = React.useState<string | null>(null);
  const [selectedCustomizations, setSelectedCustomizations] =
    React.useState<SelectedCustomization>({});
  const [price, setPrice] = React.useState<number>(0);

  React.useEffect(() => {
    if (cartSearchParam) {
      const cart = JSON.parse(decodeURIComponent(cartSearchParam));
      if ("id" in cart) setProductId(cart["id"]);
      if ("customizations" in cart)
        setSelectedCustomizations(cart["customizations"]);
      if ("price" in cart) setPrice(cart["price"]);
    }
  }, [cartSearchParam]);

  if (!cartSearchParam)
    return <Typography>Cart is empty. Nothing to checkout.</Typography>;

  if (!productId) return <Typography>Loading...</Typography>;

  const product = getSearchProduct(productId);
  if (!product) return <Typography>This product does not exist.</Typography>;

  return (
    <>
      <Typography variant="h5">Checkout</Typography>
      <Typography fontWeight="bold" variant="h6">
        Cart
      </Typography>
      <Typography>Item: {product.name}</Typography>
      <Typography>
        Customizations:{" "}
        {Object.keys(selectedCustomizations)
          .map(
            (customization) =>
              `${customization} (${selectedCustomizations[customization]})`
          )
          .join(", ")}
      </Typography>
      <Typography>Price: ${price.toFixed(2)}</Typography>

      <Typography fontWeight="bold" variant="h6">
        Order
      </Typography>
      <FormContainer
        fields={[
          ["firstName", "lastName"],
          "streetAddress",
          ["city", "state", "zipCode"],
        ]}
        submitLabel="Order"
        onSubmit={(formValuesString) => {
          navigateTo({
            router,
            url: `/playground/thanks?cart=${stringifyJsonSortKeys({
              id: productId,
              customizations: selectedCustomizations,
            })}&location=${formValuesString}`,
          });
        }}
        dontLogSubmit
      />
    </>
  );
}
