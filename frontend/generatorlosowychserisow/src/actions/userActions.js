import { loginapi } from "../api/userApi";

export const LOG_IN = "LOG_IN";
export const WRONG_LOG_IN = "WRONG_LOG_IN";
export const LOG_OUT = "LOG_OUT";
export const AUTO_LOG_IN = "AUTO_LOG_IN";

// Action Creators

const logIn = (payload) => ({ type: LOG_IN, payload });
const wrongLogIn = (payload) => ({ type: WRONG_LOG_IN, payload });
export const logOut = () => ({ type: LOG_OUT });

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
      //we only get here if there is no error
    })
    .then((data) => {
      dispatch(logIn(data));
    })
    .catch((err) => {
      console.log(err);
    });
};

export const autoLogin = () => (dispatch) => {
  fetch(`${loginapi}api/auth/token/verify/`, {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      //Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    body: JSON.stringify(`Bearer ${localStorage.getItem("token")}`),
  })
    .then((res) => res.json())
    .then((data) => {
      localStorage.setItem("token", data.token);
      dispatch(logIn(data.user));
    });
};
