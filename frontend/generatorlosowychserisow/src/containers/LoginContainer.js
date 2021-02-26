import React from "react";
import LoginForm from "../Components/LoginForm/LoginForm";
import "./LoginContainer.scss";
import Paper from "@material-ui/core/Paper";

function LoginContainer() {
  return (
    <div className="LoginContainer">
      <Paper className="LoginPaper" elevation={7}>
        <div className="LoginPaperMargin">
          <LoginForm />
        </div>
      </Paper>
    </div>
  );
}

export default LoginContainer;
