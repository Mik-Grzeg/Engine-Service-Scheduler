import React, { useState, useEffect } from "react";
import { connect } from "react-redux";
import Container from "@material-ui/core/Container";
import CompanyPageBase from "../Components/ComapnyPageBase/CompanyPageBase";
import Grid from "@material-ui/core/Grid";
import CompanyPage from "../Components/ComapnyPage/CompanyPage";
import TextField from "@material-ui/core/TextField";
import Autocomplete from "@material-ui/lab/Autocomplete";
import { fetchCompanyList, fetchCompanyById } from "../actions/companyActions";

export const CompanyContainer = ({
  companyList,
  fetchCompanyList,
  fetchCompanyById,
}) => {
  const [value, setValue] = useState(null);
  const [inputValue, setInputValue] = useState("");

  useEffect(() => {
    fetchCompanyList();
  }, []);

  useEffect(() => {
    if (value !== null) {
      console.log(value.id);
      fetchCompanyById(value.id);
    }
  }, [value]);
  return (
    <Container maxWidth={false}>
      <div className="backgroundCompany">
        <Grid
          container
          direction="row"
          justify="center"
          alignItems="flex-start"
        >
          <Grid item>
            {" "}
            <Autocomplete
              value={value}
              onChange={(event, newValue) => {
                setValue(newValue);
              }}
              inputValue={inputValue}
              onInputChange={(event, newInputValue) => {
                setInputValue(newInputValue);
              }}
              id="controllable-states-demo"
              options={companyList}
              getOptionLabel={(option) => option.name}
              style={{ minWidth: 180, maxWidth: 300 }}
              renderInput={(params) => (
                <TextField {...params} label="Compnies" variant="outlined" />
              )}
            />
          </Grid>
        </Grid>
        <Grid container direction="column" justify="center" alignItems="center">
          <Grid item> jestem danymi firm i ciane sie na sam dol </Grid>
        </Grid>
      </div>
    </Container>
  );
};

const mapStateToProps = (state) => ({
  companyList: state.companyReducer.companyList,
});
const mapDispatchToProps = (dispatch) => {
  return {
    fetchCompanyList: () => dispatch(fetchCompanyList()),
    fetchCompanyById: (id) => dispatch(fetchCompanyById(id)),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(CompanyContainer);
