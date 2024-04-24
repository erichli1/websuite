"use client";

import { FormContainer } from "@/ui/containers/Forms";
import { Typography } from "@mui/material";
import { navigateTo } from "../playgroundUtils";
import { useRouter } from "next/navigation";

export default function Page() {
  const router = useRouter();

  return (
    <>
      <Typography variant="h5">Checkout</Typography>
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
            url: `/playground/thanks?submitted=${formValuesString}`,
          });
        }}
        dontLogSubmit
      />
    </>
  );
}
