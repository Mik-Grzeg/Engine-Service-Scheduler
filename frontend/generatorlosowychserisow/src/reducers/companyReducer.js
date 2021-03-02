import { DOWNLOAD_LIST, DOWNLOAD_COMPANY } from "../actions/companyActions";

const defaultState = {
  companyList: [
    { name: "cos tam 1", id: 1 },
    { name: "cos tam 2", id: 2 },
    { name: "cos tam 3", id: 3 },
  ],
  isCompanyDowloaded: true,
  company: {
    name: "NAME",
    contact: "+48000000000",
    installation_set: [],
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

/*export function rootLevelReducer(state, action){
    return {
        ...state,
        firstLevel: {
            ...state.firstLevel,
            secondLevel: {
                ...state.firstLevel.secondLevel,
                thirdLevel: {
                    ...state.firstLevel.secondLevel.thirdLevel,
                    property1: action.data
                }
            }
        }
    }
} */
