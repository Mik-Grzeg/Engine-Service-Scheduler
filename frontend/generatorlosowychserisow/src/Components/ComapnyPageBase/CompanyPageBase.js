import React from "react";
import { connect } from "react-redux";
import Grid from "@material-ui/core/Grid";
import Skeleton from "@material-ui/lab/Skeleton";

//TO DO SKELETON OF CARDS

export const CompanyPageBase = (props) => {
  return (
    <Grid
      container
      direction="column"
      justify="space-evenly"
      alignItems="stretch"
    >
      <Grid item>
        {" "}
        COMAPNY PAGE BASE _ THHIS IS GHOING TO BE DISPLAYED BY DEFAULT ON
        COMPANY CONTAINER IF USER CLICK ANNY OF COMPANIES HE WONT SEE IT
      </Grid>
    </Grid>
  );
};

const mapStateToProps = (state) => ({});

const mapDispatchToProps = () => {};

export default connect(mapStateToProps)(CompanyPageBase);
