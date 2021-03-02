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
    permison: 0,
  },
};

const userReducer = (state = defaultState, action) => {
  // send tokens to the localstorage and all user info into user object
  if (action.type === LOG_IN) {
    localStorage.setItem("access", action.payload.access);
    localStorage.setItem("refresh", action.payload.refresh);
    return {
      ...state,
      loggedIn: true,
      user: {
        ...state.user,
        name: action.payload.first_name,
      },
    };
  }
  // if the responce in log in was 401 sets errorLogIn to be true chaing the color of textFields in login form
  if (action.type === WRONG_LOG_IN) {
    return { ...state, loggedIn: false, errorLogIn: true, user: {} };
  }
  // removes all data from local storeage and sets user to empty object
  if (action.type === LOG_OUT) {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    return { ...state, loggedIn: false, user: {} };
  }
  //after user reenter the side with the token in local storage and if token is valid
  //log in user auutomatyly and dowload the use credentails
  if (action.type === AUTO_LOG_IN) {
    return { ...state, loggedIn: true, user: { ...state.user } };
  }
  return { ...state };
};

export default userReducer;
