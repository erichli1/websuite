"use client";

import { FormContainer } from "@/ui/containers/Forms";
import { Typography } from "@mui/material";

export default function Page() {
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
      />
    </>
  );
}
