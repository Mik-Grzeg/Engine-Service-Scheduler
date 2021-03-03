import React, { useState } from "react";
import { connect } from "react-redux";

import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import CardActions from "@material-ui/core/CardActions";
import CardContent from "@material-ui/core/CardContent";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import ComapnyCardInstallation from "../CompanyCardInstallation/ComapnyCardInstallation";

export const CompanyPage = ({ company }) => {
  console.log(company);
  return (
    <Grid
      container
      direction="row"
      justify="flex-start"
      alignItems="flex-start"
      style={{ marginTop: "12px" }}
      spacing={1}
    >
      <Grid item xs={12} md={6} xl={4}>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              COMPANY_INFO
            </Typography>
            <Typography variant="h5" component="h2">
              {company.name}
            </Typography>
            <Typography color="textSecondary">adjective</Typography>
            <Typography variant="body2" component="p">
              well meaning and kindly.
              <br />
              {'"a benevolent smile"'}
            </Typography>
          </CardContent>
          <CardActions>
            <Button size="small">Learn More</Button>
          </CardActions>
        </Card>
      </Grid>
      <Grid item xs={12} md={6} xl={8}>
        <Grid
          container
          direction="column"
          justify="flex-start"
          alignItems="stretch"
          spacing={1}
        >
          {company.installation_set.map((installation, index) => {
            return (
              <Grid item xs={12} key={index}>
                <ComapnyCardInstallation installation={installation} />
              </Grid>
            );
          })}
        </Grid>
      </Grid>
    </Grid>
  );
};

const mapStateToProps = (state) => ({
  company: state.companyReducer.company,
});

export default connect(mapStateToProps)(CompanyPage);
