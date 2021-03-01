import { DOWNLOAD_LIST, DOWNLOAD_COMPANY } from "../actions/companyActions";

const defaultState = {
  companyList: [
    { name: "cos tam 1", id: 1 },
    { name: "cos tam 2", id: 2 },
    { name: "cos tam 3", id: 3 },
  ],
  isCompanyDowloaded: false,
  company: {
    name: "NAME",
    contact: "+48000000000",
    installation_set: [{ installation_name: "installation_name 1" }],
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
        contant: action.payload.contant,
        installation_set: [
          {
            ...state.company.installation_set,
            installation_name: action.payload.installation_set,
          },
        ],
      },
    };
  }
  return { ...state };
};

export default companyReduser;

{
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
}
