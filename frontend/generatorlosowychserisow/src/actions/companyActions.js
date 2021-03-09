import { loginapi } from "../api/userApi";
import { refresh } from "./userActions";
// Redux Variables
export const DOWNLOAD_LIST = "DOWNLOAD_LIST";
export const DOWNLOAD_COMPANY = "DOWNLOAD_COMPANY";

const dowloadList = (payload) => ({ type: DOWNLOAD_LIST, payload });
const downloadCompany = (payload) => ({ type: DOWNLOAD_COMPANY, payload });

// Methods

// Function do fetch list of all companies in data base
// this list is stored in redux store
// Format [{id,name}]
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
      if (err.status === 401) {
        dispatch(refresh());
        if (localStorage.getItem("access") !== null) {
          dispatch(fetchCompanyList);
        }
      }
    });
};
// Function to fetch i commpany chosen from the list
// it takes id of company to get all data about it
// format {name,contact,installation_set {installatuion_name , installation_location , engine contract_set{ id ,contract_start ,contract_end} }}
export const fetchCompanyById = (id) => (dispatch) => {
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
      dispatch(downloadCompany(data));
    })
    .catch((err) => {
      if (err.status === 401) {
        dispatch(refresh());
        if (localStorage.getItem("access") !== null) {
          dispatch(fetchCompanyById(id));
        }
      }
    });
};
