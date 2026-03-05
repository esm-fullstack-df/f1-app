import {
  Show,
  TextField,
  DataTable,
  List,
  UrlField
} from "react-admin";

import Grid from "@mui/material/Grid";

import {
  FilenameImageField
} from "./common.tsx"

export const CircuitList = () => (
  <List>
    <DataTable>
      <DataTable.Col source="id" />
      <DataTable.Col source="circuit_ref" />
      <DataTable.Col source="name" />
      <DataTable.Col source="location" />
      <DataTable.Col source="country" />
      <DataTable.Col source="lat" />
      <DataTable.Col source="lng" />
      <DataTable.Col source="url">
        <UrlField source="url" />
      </DataTable.Col>
      <DataTable.Col source="image" />
    </DataTable>
  </List>
);

export const CircuitShow = () => (
  <Show>
    <Grid container spacing={2}>
      <Grid item size={6}>
        <FilenameImageField source="image" />
      </Grid>
      <Grid item size={2}>
        <TextField source="name" />
      </Grid>
      <Grid item size={2}>
        <TextField source="location" />
      </Grid>
      <Grid item size={2}>
        <TextField source="country" />
      </Grid>
    </Grid>
  </Show>
);