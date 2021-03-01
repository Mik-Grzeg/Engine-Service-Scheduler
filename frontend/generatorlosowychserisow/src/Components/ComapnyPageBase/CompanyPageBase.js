import React from "react";
import { connect } from "react-redux";
import Grid from "@material-ui/core/Grid";

export const CompanyPageBase = (props) => {
  return (
    <Grid
      container
      direction="column"
      justify="space-evenly"
      alignItems="stretch"
    >
      <Grid item> cos tam</Grid>
      <Grid item> cos tam</Grid>
      <Grid item> cos tam</Grid>
    </Grid>
  );
};

const mapStateToProps = (state) => ({});

const mapDispatchToProps = {};

export default connect(mapStateToProps, mapDispatchToProps)(CompanyPageBase);
