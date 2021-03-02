import {
  LOG_IN,
  LOG_OUT,
  AUTO_LOG_IN,
  WRONG_LOG_IN,
} from "../actions/userActions";

const defaultState = {
  loggedIn: true,
  requierdEmail: "@mail.com",
  errorLogIn: false,
  user: {
    name: "user_testowy",
    access_token: "",
    refresh_token: "",
    permison: 0,
  },
};

const userReducer = (state = defaultState, action) => {
  if (action.type === LOG_IN) {
    localStorage.setItem("access", action.payload.access);
    localStorage.setItem("refresh", action.payload.refresh);
    return {
      ...state,
      loggedIn: true,
      user: {
        ...state.user,
        name: action.payload.first_name,
        access_token: action.payload.access,
        refresh_token: action.payload.refresh,
      },
    };
  }
  if (action.type === WRONG_LOG_IN) {
    return { ...state, loggedIn: false, errorLogIn: true, user: {} };
  }

  if (action.type === LOG_OUT) {
    console.log("eyy");
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    return { ...state, loggedIn: false, user: {} };
  }

  if (action.type === AUTO_LOG_IN) {
    return { ...state, loggedIn: true, user: { ...state.user } };
  }
  return { ...state };
};

export default userReducer;
