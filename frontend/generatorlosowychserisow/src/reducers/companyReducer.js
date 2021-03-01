import { DOWNLOAD_LIST, DOWNLOAD_COMPANY } from "../actions/companyActions";

const defaultState = {
  companyList: [
    { name: "cos tam 1", id: 1 },
    { name: "cos tam 2", id: 2 },
    { name: "cos tam 3", id: 3 },
  ],
  company: {
    name: "NAME",
    localisation: "LOCATISATION",
  },
};

const companyReduser = (state = defaultState, action) => {
  if (action.type === DOWNLOAD_LIST) {
    return { ...state, companyList: action.payload };
  }

  if (action.type === DOWNLOAD_COMPANY) {
    return { ...state, company: action.payload };
  }
  return { ...state };
};

export default companyReduser;
