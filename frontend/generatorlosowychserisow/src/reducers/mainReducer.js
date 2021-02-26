import userReducer from "./userReducer";
import companyReducer from "./companyReducer";
import { combineReducers } from "redux";

const mainReducer = combineReducers({
  userReducer,
  companyReducer,
});

export default mainReducer;
