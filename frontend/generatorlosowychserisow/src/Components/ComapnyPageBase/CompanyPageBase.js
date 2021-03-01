import React from "react";
import { connect } from "react-redux";

export const CompanyPageBase = (props) => {
  return <div style={{ backgroundColor: "red" }}> cos tam, cos</div>;
};

const mapStateToProps = (state) => ({});

const mapDispatchToProps = {};

export default connect(mapStateToProps, mapDispatchToProps)(CompanyPageBase);
