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

export const ConstructorList = () => (
  <List>
    <DataTable>
      <DataTable.Col source="id" />
      <DataTable.Col source="constructor_ref" />
      <DataTable.Col source="name" />
      <DataTable.Col source="nationality" />
      <DataTable.Col source="url">
        <UrlField source="url" />
      </DataTable.Col>
      <DataTable.Col source="image" />
    </DataTable>
  </List>
);

export const ConstructorShow = () => (
  <Show>
    <Grid container spacing={2}>
      <Grid item xs={8}>
        <FilenameImageField source="image" />
      </Grid>
      <Grid item xs={2}>
        <TextField source="name" />
      </Grid>
      <Grid item xs={2}>
        <TextField source="nationality" />
      </Grid>
    </Grid>
  </Show>
);