import React from "react";
import { connect } from "react-redux";
import Container from "@material-ui/core/Container";
import CompanyList from "../Components/CompanyList/CompanyList";
import CompanyPageBase from "../Components/ComapnyPageBase/CompanyPageBase";
import Grid from "@material-ui/core/Grid";
import CompanyPage from "../Components/ComapnyPage/CompanyPage";

export const CompanyContainer = (props) => {
  return (
    <Container maxWidth="xl">
      <div className="backgroundCompany">
        <Grid
          container
          direction="row"
          justify="flex-start"
          alignItems="flex-start"
        >
          <Grid item xs={12} md={2}>
            <CompanyList />
          </Grid>
          <Grid item xs={12} md={10}>
            <CompanyPageBase />
          </Grid>
        </Grid>
      </div>
    </Container>
  );
};

const mapStateToProps = (state) => ({});

const mapDispatchToProps = {};

export default connect(mapStateToProps, mapDispatchToProps)(CompanyContainer);
