"use client";

import { Stack, Typography } from "@mui/material";
import {
  SelectedCustomization,
  getSearchProduct,
  navigateTo,
} from "../../playgroundUtils";
import LoggedButton from "@/ui/components/click/button/LoggedButton";
import { useRouter } from "next/navigation";
import React from "react";

export default function Page({ params }: { params: { id: string } }) {
  const product = getSearchProduct(params.id);

  const router = useRouter();

  const [selectedCustomizations, setSelectedCustomizations] =
    React.useState<SelectedCustomization>({});
  const [price, setPrice] = React.useState<number>(0);

  React.useEffect(() => {
    if (product) {
      const customizations = Object.keys(product.customizations);
      const initialCustomizations: SelectedCustomization = {};
      for (const customization of customizations)
        initialCustomizations[customization] =
          product.customizations[customization][0].name;

      setSelectedCustomizations(initialCustomizations);
      setPrice(product.basePrice);
    }
  }, [product]);

  if (!product) return <Typography>This product does not exist.</Typography>;

  return (
    <>
      <Typography variant="h5">{product.name}</Typography>

      <Typography variant="h6">${price.toFixed(2)}</Typography>

      <Typography>{product.description}</Typography>

      {Object.keys(product.customizations).map((customization) => (
        <div key={customization}>
          <Typography>
            Select {customization} ({selectedCustomizations[customization]}{" "}
            selected)
          </Typography>
          <Stack direction="row" spacing={1} sx={{ paddingY: "0.5rem" }}>
            {product.customizations[customization].map((option) => (
              <LoggedButton
                key={`${customization}-${option.name}`}
                logLabel={`${option.name} (+${option.price.toFixed(2)})`}
                variant="outlined"
                afterLog={() => {
                  setSelectedCustomizations((prev) => ({
                    ...prev,
                    [customization]: option.name,
                  }));
                  setPrice(
                    (prev) =>
                      prev +
                      option.price -
                      (product.customizations[customization].find(
                        (option) =>
                          option.name === selectedCustomizations[customization]
                      )?.price ?? 0)
                  );
                }}
                disabled={option.name === selectedCustomizations[customization]}
              />
            ))}
          </Stack>
        </div>
      ))}

      <div>
        <LoggedButton
          logLabel="Buy now"
          variant="contained"
          afterLog={() =>
            navigateTo({
              router,
              url: `/playground/checkout?cart=${JSON.stringify({
                id: product.id,
                customizations: selectedCustomizations,
                price,
              })}`,
            })
          }
        />
      </div>
    </>
  );
}
