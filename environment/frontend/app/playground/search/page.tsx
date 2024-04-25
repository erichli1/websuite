"use client";

import { Box, Divider, Typography } from "@mui/material";
import { useSearchParams } from "next/navigation";
import { searchProducts } from "../playgroundUtils";
import LoggedLink from "@/ui/components/click/link/LoggedLink";

export default function Page() {
  const searchParams = useSearchParams();
  const query = searchParams.get("query");
  const results = searchProducts(query);

  return (
    <>
      <Typography variant="body1">
        Showing {results.length} results for &quot;{query}&quot;
      </Typography>

      <Divider />

      {results.map((result) => (
        <Box key={result.id}>
          <LoggedLink
            href={`/playground/product/${result.id}`}
            logLabel={result.name}
          />
          <Typography variant="body1">
            Starts at ${result.basePrice.toFixed(2)}
          </Typography>
        </Box>
      ))}
    </>
  );
}
