import {
  DataGrid,
  GridColDef,
  GridFilterModel,
  GridRowId,
  GridRowSelectionModel,
  GridSortModel,
  GridToolbar,
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

  const [filterModel, setFilterModel] = React.useState<GridFilterModel>({
    items: [],
  });

  const [sortModel, setSortModel] = React.useState<GridSortModel>([]);

  const getRowFromId = (id: GridRowId) => {
    return rows.find((row) => row.id === id);
  };

  return (
    <DataGrid
      rows={rows}
      columns={columns.map((column) => ({ ...column, flex: 1 }))}
      rowSelectionModel={rowSelectionModel}
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
      filterModel={filterModel}
      onFilterModelChange={(newFilterModel) => {
        log({
          component: "click/gridfilter",
          label: gridLogLabel,
          newVal: extractFiltersForLogAsJSON(newFilterModel),
          oldVal: extractFiltersForLogAsJSON(filterModel),
        });
        setFilterModel(newFilterModel);
      }}
      filterDebounceMs={500}
      sortModel={sortModel}
      onSortModelChange={(newSortModel) => {
        log({
          component: "click/gridsort",
          label: gridLogLabel,
          newVal: JSON.stringify(newSortModel),
          oldVal: JSON.stringify(sortModel),
        });
        setSortModel(newSortModel);
      }}
      slots={{ toolbar: GridToolbar }}
    />
  );
}

const extractFiltersForLogAsJSON = (filterModel: GridFilterModel) => {
  return JSON.stringify(
    filterModel.items.map((item) => ({
      field: item.field,
      operator: item.operator,
      value: item.value,
    }))
  );
};
