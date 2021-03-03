import { DOWNLOAD_LIST, DOWNLOAD_COMPANY } from "../actions/companyActions";

const defaultState = {
  companyList: [
    { name: "cos tam 1", id: 1 },
    { name: "cos tam 2", id: 2 },
    { name: "cos tam 3", id: 3 },
  ],
  isCompanyDowloaded: false,
  company: {
    name: "COMAPNY_NAME",
    contact: "+48000000000",
    installation_set: [
      {
        installation_name: "kopalnia 1",
        installation_location: "katowice 1",
        engine: {
          id: 3,
          serial_number: "dsajdiosaiodsau",
          type: "2",
        },
        // DATE fomrat YYYY-MM-DD
        contract_set: [
          {
            id: 1122,
            contract_start: "2010-12-08",
            contract_end: "2014-12-08",
          },
          {
            id: 1123,
            contract_start: "2014-12-09",
            contract_end: "2018-12-08",
          },
          {
            id: 1124,
            contract_start: "2018-12-09",
            contract_end: "2022-12-08",
          },
        ],
      },
      {
        installation_name: "kopalnia 2",
        installation_location: "katowice 11",
        engine: {
          id: 3,
          serial_number: "dsajdiosaiodsau",
          type: "2",
        },
        contract_set: [
          {
            id: 2122,
            contract_start: "2009-12-08",
            contract_end: "2013-12-08",
          },
          {
            id: 2123,
            contract_start: "2013-12-09",
            contract_end: "2015-12-08",
          },
          {
            id: 2124,
            contract_start: "2015-12-09",
            contract_end: "2023-12-08",
          },
        ],
      },
    ],
  },
};

const companyReduser = (state = defaultState, action) => {
  if (action.type === DOWNLOAD_LIST) {
    return { ...state, companyList: action.payload };
  }

  if (action.type === DOWNLOAD_COMPANY) {
    return {
      ...state,
      isCompanyDowloaded: true,
      company: {
        ...state.company,
        name: action.payload.name,
        contact: action.payload.contact,
        installation_set: action.payload.installation_set.map((item) => {
          return {
            installation_name: item.installation_name,
            installation_location: item.installation_location,
            // TO DO ITS NOT ALWAYS GONNA BE FULL BUT ITS GOING TO BE ONE ITEM
            engine: item.engine,
            contract_set: item.contract_set.map((contract) => {
              return {
                id: contract.id,
                contract_start: contract.contract_start,
                contract_end: contract.contract_end,
              };
            }),
          };
        }),
      },
    };
  }
  return { ...state };
};

export default companyReduser;
