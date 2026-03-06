import {
  FunctionField,
} from "react-admin";

// component that constructs an image link hosted by the API based on filename in "image" field of given record
// used in Show on circuits, constructors, and drivers pages
export const FilenameImageField = () => (
  <FunctionField 
    render={record => 
      record.image ? (
        <img src={`http://localhost:9000/images/${record.image}`} style={{ maxHeight: '250px' }} alt='Image' title='Image' />
      ) : null
    } 
  />
);