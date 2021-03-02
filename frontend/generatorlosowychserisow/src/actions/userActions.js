import { loginapi } from "../api/userApi";

//ACTION SEND TO REDUX
export const LOG_IN = "LOG_IN";
export const SET_USER = "SET_USER";
export const WRONG_LOG_IN = "WRONG_LOG_IN";
export const LOG_OUT = "LOG_OUT";
export const AUTO_LOG_IN = "AUTO_LOG_IN";

// Action Creators

const logIn = (payload) => ({ type: LOG_IN, payload });
const autoLogIn = () => ({ type: AUTO_LOG_IN });
const setUser = (payload) => ({ type: SET_USER, payload });
const wrongLogIn = (payload) => ({ type: WRONG_LOG_IN, payload });

// Methods

//Removes access and refresh tokens from memory
export const logOut = () => ({ type: LOG_OUT });

// After Looginng in function send access token to get basic info about user
// Name Email Groups and Permison and set them in store
export const fetchUserData = () => (dispatch) => {
  fetch(`${loginapi}api/auth/user/me/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("access")}`,
    },
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data);
      dispatch(setUser(data));
    })
    .catch((err) => {
      console.log(err);
    });
};

// Funcion to log user into the system
// It takes email and password as json data ]
// It dispatches Access and Refresh Token
export const fetchUser = (userInfo) => (dispatch) => {
  fetch(`${loginapi}api/auth/login/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ ...userInfo }),
  })
    .then((response) => {
      if (!response.ok) {
        dispatch(wrongLogIn());
        throw response;
      } else {
        return response.json();
      }
    })
    .then((data) => {
      dispatch(logIn(data));
    })
    .catch((err) => {
      console.log(err);
    });
};

// Functiopn to log user into a system if the access token is already in memory
// It dispaches a change of status to logged in
// if the token is invalid or expired it removes it from local memory
export const autoLogin = () => (dispatch) => {
  const token = { token: localStorage.getItem("access") };
  fetch(`${loginapi}api/auth/token/verify/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify({ ...token }),
  }).then((res) => {
    if (res.ok) {
      dispatch(autoLogIn());
    } else {
      dispatch(logOut());
    }
  });
};
