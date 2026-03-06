import {
  DataTable,
  DateField,
  List,
  Show,
  TextField,
  UrlField,
  Edit,
  SimpleForm,
  TextInput,
  DateInput,
  Create,
  required,
} from "react-admin";

import Grid from "@mui/material/Grid";

import {
  FilenameImageField
} from "./common.tsx"

export const DriverList = () => (
  <List>
    <DataTable>
      <DataTable.Col source="id" />
      <DataTable.Col source="driver_ref" />
      <DataTable.Col source="number" />
      <DataTable.Col source="code" />
      <DataTable.Col source="forename" />
      <DataTable.Col source="surname" />
      <DataTable.Col source="dob">
        <DateField source="dob" />
      </DataTable.Col>
      <DataTable.Col source="nationality" />
      <DataTable.Col source="url">
        <UrlField source="url" />
      </DataTable.Col>
      <DataTable.Col source="image" />
    </DataTable>
  </List>
);

export const DriverShow = () => (
  <Show>
    <Grid container spacing={2}>
      <Grid item size={4}>
        <FilenameImageField source="image" />
      </Grid>
      <Grid item size={2}>
        <TextField source="forename" title="FirstName" />
      </Grid>
      <Grid item size={2}>
        <TextField source="surname" title="LastName" />
      </Grid>
      <Grid item size={2}>
        <TextField source="id" />
      </Grid>
      <Grid item size={2}>
        <TextField source="driver_ref" />
      </Grid>
      <Grid item size={2}>
        <TextField source="number" />
      </Grid>
      <Grid item size={2}>
        <TextField source="code" />
      </Grid>
      <Grid item size={2}>
        <TextField source="dob" />
      </Grid>
      <Grid item size={2}>
        <TextField source="nationality" />
      </Grid>
      <Grid item size={2}>
        <TextField source="url" />
      </Grid>
    </Grid>
  </Show>
);

// edit form, make id field readonly for clarity
export const DriverEdit = () => (
  <Edit>
    <SimpleForm>
      <TextInput readOnly source="id" />
      <TextInput source="driver_ref" />
      <TextInput source="number" />
      <TextInput source="code" />
      <TextInput source="forename" />
      <TextInput source="surname" />
      <DateInput source="dob" />
      <TextInput source="nationality" />
      <TextInput source="url" />
      <TextInput source="image" />
    </SimpleForm>
  </Edit>
);

// create form with client-side validation on required fields
export const DriverCreate = () => (
  <Create>
    <SimpleForm>
      <TextInput readOnly source="id" defaultValue={-1} />
      <TextInput source="driver_ref" validate={required()} />
      <TextInput source="number" validate={required()} />
      <TextInput source="code" validate={required()} />
      <TextInput source="forename" validate={required()} />
      <TextInput source="surname" validate={required()} />
      <DateInput source="dob" validate={required()} />
      <TextInput source="nationality" validate={required()} />
      <TextInput source="url" validate={required()} />
      <TextInput readOnly source="image" defaultValue={''}/>
    </SimpleForm>
  </Create>
);
