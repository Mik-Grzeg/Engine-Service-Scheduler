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
export const logOut = () => ({ type: LOG_OUT });

export const fetchUserData = () => (dispatch) => {
  console.log("fetch user data");
  fetch(`${loginapi}api/auth/user/me/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      Authorization: `Bearer ${localStorage.getItem("access")}`,
    },
  })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      console.log(data);
      dispatch(setUser(data));
    })
    .catch((err) => {
      console.log(err);
    });
};

// Methods

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
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
    }
  });
};
