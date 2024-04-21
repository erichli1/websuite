import {
  DataGrid,
  GridColDef,
  GridRowId,
  GridRowSelectionModel,
  GridRowsProp,
} from "@mui/x-data-grid";
import React from "react";
import { log } from "../log";

type DataGridContainerProps<T> = {
  gridLogLabel: string;
  rows: Array<T & { id: string; logLabel: string }>;
  columns: Array<Pick<GridColDef, "field" | "headerName">>;
};

export default function DataGridContainer<T>({
  gridLogLabel,
  rows,
  columns,
}: DataGridContainerProps<T>) {
  const [rowSelectionModel, setRowSelectionModel] =
    React.useState<GridRowSelectionModel>([]);

  const getRowFromId = (id: GridRowId) => {
    return rows.find((row) => row.id === id);
  };

  return (
    <DataGrid
      rows={rows}
      columns={columns.map((column) => ({ ...column, flex: 1 }))}
      onRowSelectionModelChange={(newRowSelectionModel) => {
        const newRow = getRowFromId(newRowSelectionModel[0]);
        const oldRow = getRowFromId(rowSelectionModel[0]);
        log({
          component: "click/gridselect",
          label: gridLogLabel,
          newVal: newRow?.logLabel,
          oldVal: oldRow?.logLabel,
        });
        setRowSelectionModel(newRowSelectionModel);
      }}
      rowSelectionModel={rowSelectionModel}
    />
  );
}
