"use client";

import LoggedIconButton from "@/ui/components/click/iconbutton/LoggedIconButton";
import LoggedTextField from "@/ui/components/type/text/LoggedTextField";
import { AppBarContainer } from "@/ui/containers/Appbars";
import { Search } from "@mui/icons-material";
import React from "react";
import { useRouter } from "next/navigation";
import { navigateTo } from "./playgroundUtils";
import Stack from "@mui/material/Stack";

export default function PlaygroundLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [searchQuery, setSearchQuery] = React.useState<string>("");

  const router = useRouter();

  return (
    <>
      <AppBarContainer title="Playground">
        <LoggedTextField
          logLabel="Search items"
          InputProps={{ sx: { backgroundColor: "white" } }}
          hideLabel
          placeholder="Search items"
          size="small"
          onChange={(event) => setSearchQuery(event.target.value)}
        />
        <LoggedIconButton
          logLabel="Search"
          icon={<Search />}
          color="inherit"
          afterLog={() => {
            navigateTo({
              router,
              url: `/playground/search?query=${searchQuery}`,
            });
          }}
        />
      </AppBarContainer>
      <Stack spacing={1} padding="1rem">
        {children}
      </Stack>
    </>
  );
}
