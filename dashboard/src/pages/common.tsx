import {
  FunctionField,
} from "react-admin";

export const FilenameImageField = () => (
  <FunctionField 
    render={record => 
      record.image ? (
        <img src={`http://localhost:9000/images/${record.image}`} style={{ maxHeight: '250px' }} alt='Image' title='Image' />
      ) : null
    } 
  />
);