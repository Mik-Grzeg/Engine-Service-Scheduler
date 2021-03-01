import { loginapi } from "../api/userApi";

export const DOWNLOAD_LIST = "DOWNLOAD_LIST";
export const DOWNLOAD_COMPANY = "DOWNLOAD_COMPANY";

const dowloadList = (payload) => ({ type: DOWNLOAD_LIST, payload });
const downloadCompany = (payload) => ({ type: DOWNLOAD_COMPANY, payload });

export const fetchCompanyList = () => (dispatch) => {
  fetch(`${loginapi}api/client/company/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + localStorage.getItem("access").toString(),
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw response;
      } else {
        return response.json();
      }
    })
    .then((data) => {
      dispatch(dowloadList(data));
    })
    .catch((err) => {
      console.log(err);
    });
};

export const fetchCompanyById = (id) => (dispatch) => {
  console.log(id, 1);
  fetch(`${loginapi}api/client/company/${id}/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + localStorage.getItem("access").toString(),
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw response;
      } else {
        return response.json();
      }
    })
    .then((data) => {
      console.log(data);
      dispatch(downloadCompany(data));
    })
    .catch((err) => {
      console.log(err);
    });
};
