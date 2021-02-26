import { LOG_IN, LOG_OUT, AUTO_LOG_IN } from "../actions/userActions";

const defaultState = {
  loggedIn: false,
  requierdEmail: "@gmail.com",
  user: {
    name: "",
    access_token: "",
    refresh_token: "",
    permison: 0,
  },
};

const userReducer = (state = defaultState, action) => {
  if (action === LOG_IN) {
    return { ...state, loggedIn: true, user: { ...state.user } };
  }

  if (action === LOG_OUT) {
    return { ...state, loggedIn: false, user: {} };
  }

  if (action === AUTO_LOG_IN) {
    return { ...state, loggedIn: false, user: { ...state.user } };
  }
  return { ...state };
};

export default userReducer;
